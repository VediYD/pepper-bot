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
data['content'] = data['course_name'] + ' ' + data.o_summarized
loader = DataFrameLoader(data[['content']], page_content_column='content') 
document = loader.load_and_split()
print('context document loaded')

def finalize_batch():
    global to_send
    to_send.append(''.join(responses).split('.')[-2])


def _callback(token_id: int, response: str) -> bool:
    global counter, responses, _nsent
    
    # save the summary tokens
    responses.append(response.decode('utf-8'))
    
    if '.' in response.decode('utf-8'):
        # every time a . is detected is a new sentence
        counter += 1
        finalize_batch()
    
    # if the total number of sentences are less than 2
    if counter < 3:
        _nsent = False
        # continue generation process
        return True
    
    else:
        # reset sentence counter
        counter = 0
        _nsent = True
        
        # stop further generation
        return False

# load the embeddings to store the sentence transformations and search results
embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
db = Chroma.from_documents(document, embeddings,)
print('embeddings loaded for sentence similarity search')

# load the model that would be used to generate the responses
# load the model
counter = 0
responses = []
to_send = []
_nsent = False
model_path = '/app/ggml-gpt4all-j-v1.3-groovy.bin'
llm = GPT4All(model=model_path, verbose=False, n_threads=8, seed=42, temp=0.3, streaming=False, use_mlock=True)
llm.client.model._response_callback = _callback
print('GPT4ALL model loaded - 1.3 groovy')

# create the prompt template and create the QA object
# declare the prompt template
template = """
Use the context provided below and give an answer in a 3 sentence answer. 
Context: {context}
Question: {question} 
Answer:  The relevant courses are
"""
PROMPT = PromptTemplate(
    template=template, input_variables=["context", "question"]
)

qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type='stuff',
    retriever=db.as_retriever(),
    chain_type_kwargs={"prompt": PROMPT},
    return_source_documents=True,
    verbose=False,
)
print('QA object initialized')
app = Flask(__name__)


@app.route('/courseInfo', methods=['POST'])
def handle_question():
    data = request.get_json()  # Assuming the question is sent as a JSON payload
    question = data['question']
    
    global counter, responses, to_send, _nsent, db
    counter = 0
    responses = []
    to_send = []
    
    def yield_generation():
        global db
#         _te = []
#         for i in db.similarity_search(question):
#             _te.append(i.metadata['course_code'])
            
#         yield ','.join(_te)
        
        index = 0 
        while True:
            lres = len(to_send)
            if (index+1) <= lres:
                yield to_send[index]
                index += 1
            if _nsent:
                yield "quit"
                break
            
            sleep(1)
    
    
    def task():
        qa(question)
    
    th = threading.Thread(target=task)
    th.start()
    
    # Return the answer as a JSON response
    return Response(yield_generation(), mimetype='application/json')


if __name__ == '__main__':
    print('Spinning Servers')
    app.run(host='0.0.0.0', port=8891, debug=False)