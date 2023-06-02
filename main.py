import fileinput

import matplotlib as matplotlib
import requests
from Cython import inline
from skimage.transform import resize
from flask import Flask,render_template,request,flash,Response
import os
import matplotlib
import tensorflow as tf
from matplotlib import pyplot as plt
import numpy as np
import tensorflow_hub as hub
import cv2
from IPython.display import Image

import io
from flask import Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from flask import Flask
import numpy as np

app=Flask(__name__)
app.secret_key="123"

app.config['UPLOAD_FOLDER']="static/images/"
app.config['UPLOAD_FOLDER1']="static/images1/"

@app.route("/",methods=['GET','POST'])
def upload():
    global filepath
    if request.method=='POST':
        upload_image=request.files['upload_image']

        if upload_image.filename!='':
            filepath=os.path.join(app.config["UPLOAD_FOLDER"],upload_image.filename)
            upload_image.save(filepath)
            #path=filepath
            return render_template('upload.html',path=filepath)
            flash("File Upload Successfully","success")

    return render_template("upload.html")

@app.route('/second')
def second():
    return render_template("upload1.html")

@app.route("/he",methods=['GET','POST'])
def upload1():
    global filepath1
    if request.method=='POST':
        upload_image1=request.files['upload_image1']

        if upload_image1.filename!='':
            filepath1=os.path.join(app.config["UPLOAD_FOLDER1"],upload_image1.filename)
            upload_image1.save(filepath1)
            #path=filepath
        return render_template('upload1.html',path1=filepath1)
        flash("File Upload Successfully","success")
    #return render_template("upload1.html")
    return render_template('upload1.html')

@app.route('/convert',methods=['GET','POST'])
def convert():
   content_image = load_image(img_path=filepath)
   style_image = load_image(img_path=filepath1)
   stylized_image = model(tf.constant(content_image), tf.constant(style_image))[0]
   plt.imshow(np.squeeze(stylized_image))
   plt.savefig(r"C:\Users\Acer\Pictures\Ai_image_test")
   return render_template('upload1.html')

model = hub.load('https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2')

def load_image(img_path):
    img = tf.io.read_file(img_path)
    img = tf.image.decode_image(img, channels=3)
    img = tf.image.convert_image_dtype(img, tf.float32)
    img = img[tf.newaxis, :]
    return img

#ff = plt
#ff.show()

if __name__ == '__main__':
    app.run(debug=True)