# built-in imports

# installed imports
from langchain.chains           import RetrievalQA
from langchain.llms             import GPT4All
from langchain.embeddings       import HuggingFaceEmbeddings
from langchain.vectorstores     import Chroma
from langchain.prompts          import PromptTemplate
from langchain.document_loaders import CSVLoader

from pandas import read_csv

from flask import Flask, request, jsonify, Response


print('imports complete')
# load course data
# load the data using csv loader
loader = CSVLoader(
    './gpt-summarized-info.csv', 
    source_column="overview", 
    csv_args={
        "delimiter": ",", 
        "fieldnames": [
            "course_name", "overview", 'requirements'
        ]
    },
)
documents = loader.load()
print('context document loaded')

# this still has an issue where it doesnt take just the overview column and instead uses all the columns and splits them weirdly. 
# refer the main.ipynb notebook for more information

# # split the documents into chunks of 256 characters each
# text_splitter = RecursiveCharacterTextSplitter(chunk_size=256, chunk_overlap=64)
# texts = text_splitter.split_documents(documents)
# print('context split into chunks of size 256 and overlap 64 characters')

# load the embeddings to store the sentence transformations and search results
embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
db = Chroma.from_documents(texts, embeddings,)
print('embeddings loaded for sentence similarity search')

# load the model that would be used to generate the responses
model_path = '/app/ggml-gpt4all-j-v1.3-groovy.bin'
llm = GPT4All(
    model=model_path, 
    backend='gptj',
    verbose=False, 
    n_threads=8, 
    seed=42, 
    temp=0.3, 
    streaming=False, 
    use_mlock=True
)
print('GPT4ALL model loaded - 1.3 groovy')

# create the prompt template and create the QA object
prompt_template = """
You are helping a student figure out what course to pick at Deakin university. 
You are an accompalished course advisor. Use the context provided below and give a summarized answer to the student's question. 
Context: {context}
Student Asks: {question} 
Advisor Responds: Yes! I can help you figure out which course would be relevant for you. There are a total of 
"""
PROMPT = PromptTemplate(
    template=prompt_template, input_variables=["context", "question"]
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
    
    # Return the answer as a JSON response
    return Response(qa(question), mimetype='application/json')


if __name__ == '__main__':
    print('Spinning Servers')
    app.run(host='0.0.0.0', port=8891)