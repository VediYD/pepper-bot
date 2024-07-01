# built-in imports

# installed imports
from langchain.chains           import RetrievalQA
from langchain.llms             import GPT4All
from langchain.embeddings       import HuggingFaceEmbeddings
from langchain.vectorstores     import Chroma
from langchain.prompts          import PromptTemplate
from langchain.document_loaders import DataFrameLoader
from pandas                     import read_csv
from time                       import time, sleep
from flask                      import Flask, request, jsonify, Response
import threading
import numpy                    as np
from scipy.io                   import wavfile
import noisereduce              as nr
import tensorflow as tf
import spacy
import pickle
from random import choice
import string

print('imports complete')

# load course data
data = read_csv('document.csv')
loader = DataFrameLoader(data, page_content_column='course_name') 
document = loader.load_and_split()
print('context document loaded')
    
# load the embeddings to store the sentence transformations and search results
embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
db = Chroma.from_documents(document, embeddings,)
print('embeddings loaded for sentence similarity search')

def finalize_batch(_responses):
    global to_send
    to_send.append(''.join(_responses))


def _callback(token_id: int, response: str) -> bool:
    global responses
    response = response.decode('utf-8')
    # save the summary tokens
    responses.append(response)
    
    if ('.' in response) or ('!' in response) or (',' in response):
        finalize_batch(responses)
        responses = []

    return True


# create the prompt template and create the QA object
# declare the prompt templateW
counter = 0
responses = []
to_send = []
llm_done = False

model_path = '/app/gpt/ggml-gpt4all-j-v1.3-groovy.bin'
llm = GPT4All(model=model_path, verbose=False, n_threads=8, temp=0.5, streaming=False, use_mlock=True)
llm.client.model._response_callback = _callback

print('GPT4ALL model loaded - 1.3 groovy')
    
prompt_template = """
Pretend that you are Pepper robot at Deakin University Open Day. 
Pepper is a humanoid robot. You are helping to answer student queries and provide entertainment.
Answer the question below and nothing else.
You may need to consider the following context: 
- Pepper is not allowed to leave the post during the event
- Pepper should not encourage people to touch them
- Pepper should refer people to the student ambassadors for physical queries, navigation help etc. if needed
Given below is the start of an interaction.
Student Says: {question}
Pepper Says: 
"""
PROMPT = PromptTemplate(
    template=prompt_template, input_variables=["question"]
)
print('QA object initialized')


def getSimilarCouses(query):
    results = db.similarity_search_with_score(query, 10)
    selected = []
    
    for doc, score in results:
        if score <= 0.95:
            selected.append(doc.metadata['course_code'])
    
    return selected

def getCourseInfo(query):
    doc, score = db.similarity_search_with_score(query, 10)[0]
    print(doc, score)
    
    if score <= 0.3:
        return doc.metadata['o_summarized'], doc.metadata['course_code']
    else:
        return '', ''


model = tf.keras.models.load_model('model/Classification.keras')
print('keras model loaded')

with open('model/label_encoder2.pkl', 'rb') as f:
    label_encoder = pickle.load(f)
print('label encoder loaded')

nlp = spacy.load("en_core_web_lg")
print('spacy language model loaded')

# initialize app
app = Flask(__name__)


# get relevant courses
@app.route('/getCourses', methods=['POST'])
def getCourses():
    """
    expected post request format
    res = post('http://172.17.0.2:8891/getCourses', json={'question':'Could you tell me about courses related to AI and Data Science?'})
    res.json()['course_codes']
    """
    # get the json
    req = request.get_json()
    
    return jsonify(course_codes=getSimilarCouses(req['question']))


@app.route('/casualQuery', methods=['POST'])
def casualQuery():
    data = request.get_json()  # Assuming the question is sent as a JSON payload
    question = data['question']
    
    global counter, responses, to_send, _nsent, llm_done
    counter = 0
    responses = []
    to_send = []
    
    def yield_generation():
        index = 0
        sent_anything = False
        start_timer = time()
        while True:
            lres = len(to_send)
            if (index+1) <= lres:
                yield to_send[index]
                index += 1
                sent_anything = True
            if llm_done:
                yield "quit"
                break
            sleep(1)
    
    
    def task():
        global llm_done
        llm_done = False
        temp = llm(PROMPT.from_template(prompt_template).format(question=question))
        llm_done = True
    
    th = threading.Thread(target=task)
    th.start()
    
    # Return the answer as a JSON response
    return Response(yield_generation(), mimetype='application/json')

# course info api
@app.route('/courseInfo', methods=['POST'])
def handle_question():
    """
    expected calling
    res = post('http://172.17.0.2:8891/courseInfo', json={'course_code':'S737'})
    res.json()['course_summary']
    """
    req = request.get_json()
    question = req['question']
    
    summary, code = getCourseInfo(question)
    print(summary, code)
    
    # Return the answer as a JSON response
    return jsonify(course_summary=summary, course_code=code)


@app.route('/denoise', methods=['POST'])
def noise_reducer():
    # Get the audio file path
    req = request.json
    rate = int(req['rate'])
    _data = np.array(req['data'])
    prop_decrease = float(req['prop_decrease'])
    vol_increase = float(req['vol_increase'])
    
    # Noise Data
    _, n_data = wavfile.read("recordings/noise.wav")

    # Reduce noise
    reduced_noise = nr.reduce_noise(y=_data, 
                                    sr=rate, 
                                    y_noise=n_data,
                                    prop_decrease=prop_decrease, 
                                    n_jobs=-1)

    # Increase volume (make up for the volume reduction)
    reduced_noise = reduced_noise * vol_increase

    # Convert to 16-bit data
    reduced_noise = reduced_noise.astype(np.int16).tolist()
    return jsonify({'rn': reduced_noise})


@app.route('/classifyResponse', methods=['POST'])
def classify_response():
    """
    res = requests.post(
        'http://10.104.23.130:8891/classifyResponse',
        json={
            'sentence': 'I want to know about courses related to AI and Data Science',
            'threshold': 0.95
        }
    )
    res.json()
    
    # Before running!
    # !pip install tensorflow==2.10.1
    # !pip install keras==2.10.0
    # !pip install spacy==3.6.1

    # You need to do this once
    # spacy.cli.download("en_core_web_lg")

    """
    res = request.json
    sentence = str(res['sentence']).lower()
    sentences = sentence.translate(str.maketrans('', '', string.punctuation))
    
    threshold = float(res['threshold'])
    sentences = nlp(sentences).vector
    predicted_labels = model.predict(np.array([sentences]))
    predicted_label = label_encoder.inverse_transform(predicted_labels.argmax(axis=1))[0]
    predicted_prob = predicted_labels[0][predicted_labels.argmax(axis=1)][0]

    if predicted_prob > threshold:
        return jsonify({'label': predicted_label, 'abv_thresh': True})

    else:
        return jsonify({'label': predicted_label, 'abv_thresh': False})


if __name__ == '__main__':
    print('Spinning Servers')
    app.run(host='0.0.0.0', port=8891, debug=False)