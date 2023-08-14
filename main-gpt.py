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

# create the prompt template and create the QA object
# declare the prompt template
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
    
    if score <= 0.2:
        return doc.metadata['o_summarized']
    else:
        return ''


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
    
    summary = getCourseInfo(question)
    print(summary)
    
    # Return the answer as a JSON response
    return jsonify(course_summary=summary)

@app.route('/noise', methods=['POST'])
def noise_reducer():
    # Get the audio file path
    data = request.json
    rate = str(data['rate'])
    data = str(data['data'])
    prop_decrease = float(data['prop_decrease'])
    vol_increase = float(data['vol_increase'])
    
    # Noise Data
    _, n_data = wavfile.read("recordings/noise.wav")

    # Reduce noise
    reduced_noise = nr.reduce_noise(y=data, 
                                    sr=rate, 
                                    y_noise=n_data,
                                    prop_decrease=prop_decrease, 
                                    n_jobs=-1)

    # Increase volume (make up for the volume reduction)
    reduced_noise = reduced_noise * vol_increase

    # Convert to 16-bit data
    reduced_noise = reduced_noise.astype(np.int16)
    return reduced_noise


if __name__ == '__main__':
    print('Spinning Servers')
    app.run(host='0.0.0.0', port=8891, debug=False)