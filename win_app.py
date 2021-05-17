from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
import webbrowser
import urllib.request
from bs4 import BeautifulSoup
from time import *
import os
import tensorflow as tf
import numpy as np
import keras
from skimage import io
from tensorflow.keras.preprocessing import image
window = Tk()
window.title("Plant Disease Detection System")
window.minsize(640,400)

model =tf.keras.models.load_model('H:\plant-leaf-detection\modeldetection.h5',compile=False)
#######################################
def openlink(url):
        webbrowser.open_new(url)
def fileDialog():
        file = filedialog.askopenfilename(initialdir =  "/", title = "Select A File", filetype =
        (("jpeg files","*.jpg"),("all files","*.*")) )
        n_img = Image.open(file)
        n_img=n_img.resize((300, 300), Image.ANTIALIAS)
        n_photo = ImageTk.PhotoImage(n_img)
        image_label.configure(image=n_photo)
        image_label.image=n_photo
        global model
        ind=model_predict(file,model)
        if(ind!=1 and ind!=4 and ind!=14):
                color="red"
        else:
                color="green"
        prediction.config(text=disease_class[ind],fg=color,font="bold")
        get_remedy(ind)
        
#################################
#Browse
browse_btn_frame=LabelFrame(window, text = "Open File",width=310,height=200)
browse_btn_frame.grid(column = 0, row = 0,columnspan=2,padx = 20)
browse_btn=Button(browse_btn_frame, text = "Browse A File",width=60,command=fileDialog)
browse_btn.grid(column = 0, row = 0,padx = 20, pady = 20)
#################################
#Prediction
prediction_frame=LabelFrame(window, text = "Prediction")
prediction_frame.grid(column = 2, row = 0,padx = 20)
prediction=Label(prediction_frame, text = "Waiting to upload",width=60)
prediction.grid(column = 0, row = 0,padx = 20, pady = 20)
#################################
#Show image



image_frame=LabelFrame(window, text = "Image",)
image_frame.grid(column = 0, row = 1,padx = 10, )
img_new = Image.open("H:\plant-leaf-detection\image-icon.png")
img_new=img_new.resize((300, 300), Image.ANTIALIAS)
photo = ImageTk.PhotoImage(img_new)
image_label=Label(image_frame, image=photo,width=330,height=330)
image_label.grid(column = 0, row = 0,padx = 20, pady = 20)

#################################
#Remedy
remedy_link=[]
remedy=[]


callback=lambda p:lambda url: webbrowser.open_new(remedy_link[p]) 
def get_remedy(ind):
       
        if(ind!=1 and ind!=4 and ind!=14):
                disease=disease_query[ind]
                try:
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
                        i=0;
                        
                        for rem in remedy:
                               
                                
                                remedy_widget=Label(remedy_frame,text=rem+"\n",justify="left", fg="blue",width=60, cursor="hand2")
                                remedy_widget.bind("<Button-1>", callback(i))
                                remedy_widget.pack()
                                i=i+1
                     
                except:
                        remedy_widget1=Label(remedy_frame,text="Bad Connection"+"\n",justify="left", fg="blue",width=60, cursor="hand2")
                        remedy_widget1.pack()

        else:
                remedy_widget1=Label(remedy_frame,text="Healthy leaf"+"\n",justify="left", fg="blue",width=60, cursor="hand2")
                remedy_widget1.pack()

remedy_frame=LabelFrame(window,text="Remedy" ,width=100,highlightthickness=2)
remedy_frame.grid(column = 2, row = 1,padx = 20, pady = 20)


print('Model loaded. ')

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



def model_predict(img_path, model):
    img = image.load_img(img_path, grayscale=False, target_size=((128,128)))
    show_img = image.load_img(img_path, grayscale=False, target_size=(128, 128))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = np.array(x, 'float32')
    x /= 255
    preds = model.predict(x)
    a = preds
    ind=np.argmax(a)
    
    
   
    return ind

mainloop()