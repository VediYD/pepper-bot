from pandas                     import read_csv
from flask                      import Flask, request, jsonify, Response
from sklearn.preprocessing      import LabelEncoder
import pickle
import numpy                    as     np
import tensorflow               as     tf
import spacy

# Initialize app
app = Flask(__name__)

@app.route('/classifyResponse', methods=['POST'])
def classify_response():

    # Before running!
    # !pip install tensorflow==2.10.1
    # !pip install keras==2.10.0
    # !pip install scapy==3.6.1

    # You need to do this once
    # spacy.cli.download("en_core_web_lg")

    res = request.json
    sentence = str(res['sentence']).lower()
    threshold = float(res['threshold'])

    try:
        model = tf.keras.models.load_model('Model/Classification_93.keras')
        nlp = spacy.load("en_core_web_lg")
        with open('Model/label_encoder.pkl', 'rb') as f:
            label_encoder = pickle.load(f)

    except Exception as e:
        print(e)
        return e
    
    sentence = nlp(sentence).vector

    predicted_labels = model.predict(np.array([sentence]))
    predicted_label = label_encoder.inverse_transform(predicted_labels.argmax(axis=1))[0]
    predicted_prob = predicted_labels[0][predicted_labels.argmax(axis=1)][0]

    if predicted_prob > threshold:
        return jsonify({'label': predicted_label, 'abv_thresh': True})

    else:
        return jsonify({'label': predicted_label, 'abv_thresh': False})

if __name__ == '__main__':
    print('Spinning Servers')
    app.run(host='0.0.0.0', port=8891, debug=False)