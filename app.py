import os
import tensorflow as tf
import numpy as np
from tensorflow import keras
from skimage import io
from tensorflow.keras.preprocessing import image
import urllib.request
from bs4 import BeautifulSoup

# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer

# Define a flask app
app = Flask(__name__)

# Model saved with Keras model.save()

# You can also use pretrained model from Keras
# Check https://keras.io/applications/

model =tf.keras.models.load_model('H:\plant-leaf-detection\modeldetection.h5',compile=False)
print('Model loaded. Check http://127.0.0.1:5000/')


def model_predict(img_path, model):
    img = image.load_img(img_path, grayscale=False, target_size=(128, 128))
    show_img = image.load_img(img_path, grayscale=False, target_size=(128, 128))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = np.array(x, 'float32')
    x /= 255
    preds = model.predict(x)
    a = preds
    ind=np.argmax(a)     
    return ind


@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')
    
disease_class=['Pepper bell Bacterial spot', 'Pepper bell healthy',
 'Potato Early blight' ,'Potato Late blight' ,'Potato healthy',
 'Tomato Bacterial spot', 'Tomato Early blight', 'Tomato Late blight',
 'Tomato Leaf Mold' ,'Tomato Septoria leaf spot',
 'Tomato Spider mites Two spotted spider mite' ,'Tomato Target Spot',
 'Tomato Yellow Leaf Curl Virus' ,'Tomato mosaic virus',
 'Tomato healthy']

disease_query=['Pepper+bell+Bacterial+spot', 'Pepper+bell+healthy',
 'Potato+Early+blight' ,'Potato+Late+blight' ,'Potato+healthy',
 'Tomato+Bacterial+spot', 'Tomato+Early+blight', 'Tomato+Late+blight',
 'Tomato+Leaf+Mold' ,'Tomato+Septoria+leaf+spot',
 'Tomato+Spider+mites+Two+spotted+spider+mite' ,'Tomato+Target+Spot',
 'Tomato+Yellow+Leaf+Curl+Virus' ,'Tomato+mosaic+virus',
 'Tomato+healthy']

@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
    
        # Get the file from post request
        print(request.files)
        f = request.files['image']
      
        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)
        
        # Make prediction
     
        prediction_index = model_predict(file_path, model)
        # print(preds[0])
        print(prediction_index)
        result={}
        print(disease_class)
        print(disease_class[prediction_index])
        result["disease"]=(disease_class[prediction_index])
        if(prediction_index!=1 and prediction_index!=4 and prediction_index!=14):
            remedy=get_remedy(prediction_index)
        else:
            remedy="NIL"
        print(remedy)
        result["remedy"]=remedy
        # x = x.reshape([64, 64]);
        # a = preds[0]
        # ind=np.argmax(a)
        # print('Prediction:', disease_class[ind])
        # result=disease_class[ind]
        return result
    return None

def get_remedy(ind):
        remedy=[]
        remedy_link=[]
       
        disease=disease_query[ind]
                
        url = 'https://google.com/search?q='+disease+'disease'+'remedies'
                                # Perform the request
        request = urllib.request.Request(url)
        request.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36')
        raw_response = urllib.request.urlopen(request).read()
        html = raw_response.decode("utf-8")
        soup = BeautifulSoup(html, 'html.parser')
        divs = soup.select("#search div.g")
                        
                        
        for div in divs:
                    results = div.select("h3")
                    if(len(results) >= 1):   
                            remedy.append(results[0].get_text())
                    link=div.select('a')
                    if(len(link) >= 1):  
                                remedy_link.append(link[0]['href'])
        return [remedy,remedy_link]             
       
                        
                     
            

  
























if __name__ == '__main__':
    app.run(port=5002, debug=True)

    # Serve the app with gevent
    # http_server = WSGIServer(('', 5000), app)
    # http_server.serve_forever()
    # app.run(debug=True)
