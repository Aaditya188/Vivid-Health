import jsonify
import requests
import pickle
import numpy as np
import sys
import os
import re
import sklearn
from flask import Flask, render_template, url_for, flash, redirect, request, send_from_directory
from sklearn.preprocessing import StandardScaler
import tensorflow
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.imagenet_utils import preprocess_input, decode_predictions
from werkzeug.utils import secure_filename

app = Flask(__name__)

model_heartdisease = pickle.load(open('heartdisease.pkl', 'rb'))
model_liverdisease = pickle.load(open('liverdisease.pkl', 'rb'))
model_cancer = pickle.load(open('breastcancer.pkl', 'rb'))
model_malaria = load_model('malariadisease.h5')
model_pneumonia = load_model('pneumonia_disease.h5')

@app.route('/',methods=['GET'])
@app.route('/home',methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/medical',methods=['GET'])
def medical():
    return render_template('medical.html')

@app.route('/heartdisease', methods=['GET','POST'])
def heartdisease():
    if request.method == 'POST':
        Age=int(request.form['age'])
        Gender=int(request.form['sex'])
        ChestPain= int(request.form['cp'])
        BloodPressure= int(request.form['trestbps'])
        ElectrocardiographicResults= int(request.form['restecg'])
        MaxHeartRate= int(request.form['thalach'])
        ExerciseInducedAngina= int(request.form['exang'])
        STdepression= float(request.form['oldpeak'])
        ExercisePeakSlope= int(request.form['slope'])
        MajorVesselsNo= int(request.form['ca'])
        Thalassemia=int(request.form['thal'])
        prediction=model_heartdisease.predict([[Age, Gender, ChestPain, BloodPressure, ElectrocardiographicResults, MaxHeartRate, ExerciseInducedAngina, STdepression, ExercisePeakSlope, MajorVesselsNo, Thalassemia]])
        if prediction==1:
            return render_template('prediction.html', prediction_text="You seem to have a Heart Disease.", greet="Oops!", title='Heart Disease')
        else:
            return render_template('prediction.html', prediction_text="You don't have any Heart Disease.", greet="Great!", title='Heart Disease')
    else:
        return render_template('heartdisease.html', title='Heart Disease')

    
@app.route('/liverdisease', methods=['GET','POST'])
def liverdisease():
    if request.method == 'POST':
        Age=int(request.form['Age'])
        Gender=int(request.form['Gender'])
        Total_Bilirubin= float(request.form['Total_Bilirubin'])
        Direct_Bilirubin= float(request.form['Direct_Bilirubin'])
        Alkaline_Phosphotase= int(request.form['Alkaline_Phosphotase'])
        Alamine_Aminotransferase= int(request.form['Alamine_Aminotransferase'])
        Aspartate_Aminotransferase= int(request.form['Aspartate_Aminotransferase'])
        Total_Protiens= float(request.form['Total_Protiens'])
        Albumin= float(request.form['Albumin'])
        Albumin_and_Globulin_Ratio= float(request.form['Albumin_and_Globulin_Ratio'])
        prediction=model_liverdisease.predict([[Age, Gender, Total_Bilirubin, Direct_Bilirubin, Alkaline_Phosphotase, Alamine_Aminotransferase, Aspartate_Aminotransferase, Total_Protiens, Albumin, Albumin_and_Globulin_Ratio]])
        if prediction==1:
            return render_template('prediction.html', prediction_text="You seem to have Liver Disease.", greet="Oops!", title='Liver Disease')
        else:
            return render_template('prediction.html', prediction_text="You don't have any Liver Disease.", greet="Great!", title='Liver Disease')
    else:
        return render_template('liverdisease.html', title='Liver Disease')

@app.route('/breastcancer', methods=['GET','POST'])
def breastcancer():
    if request.method == 'POST':
        texture_mean = float(request.form['texture_mean'])
        perimeter_mean = float(request.form['perimeter_mean'])
        smoothness_mean = float(request.form['smoothness_mean'])
        compactness_mean = float(request.form['compactness_mean'])
        concavity_mean = float(request.form['concavity_mean'])
        concave_points_mean = float(request.form['concave_points_mean'])
        symmetry_mean = float(request.form['symmetry_mean'])
        radius_se = float(request.form['radius_se'])
        compactness_se = float(request.form['compactness_se'])
        concavity_se = float(request.form['concavity_se'])
        concave_points_se = float(request.form['concave_points_se'])
        texture_worst = float(request.form['texture_worst'])
        smoothness_worst = float(request.form['smoothness_worst'])
        compactness_worst = float(request.form['compactness_worst'])
        concavity_worst = float(request.form['concavity_worst'])
        concave_points_worst = float(request.form['concave_points_worst'])
        symmetry_worst = float(request.form['symmetry_worst'])
        fractal_dimension_worst = float(request.form['fractal_dimension_worst'])
        prediction=model_cancer.predict([[texture_mean, perimeter_mean, smoothness_mean, compactness_mean,
           concavity_mean, concave_points_mean, symmetry_mean, radius_se,
           compactness_se, concavity_se, concave_points_se, texture_worst,
           smoothness_worst, compactness_worst, concavity_worst,
           concave_points_worst, symmetry_worst, fractal_dimension_worst]])
        if prediction==1:
            return render_template('prediction.html', prediction_text="The input shows the tumor is malignant.", greet="Oops!", title='Breast Cancer')
        else:
            return render_template('prediction.html', prediction_text="The input info shows the tumor is benign.", greet="Great!", title='Breast Cancer')
    else:
        return render_template('cancer.html',title='Breast Cancer')

# Image Preprocessing
def malaria_predict(img_path):
    img = image.load_img(img_path, target_size=(30, 30, 3))
    x=image.img_to_array(img)
    x=x/255
    x=np.expand_dims(x, axis=0)
    preds = model_malaria.predict(x)
    return preds

def pneumonia_predict(img_path):
    img = image.load_img(img_path, target_size=(224, 224))
    
    x=image.img_to_array(img)
    x=x/255
    x=np.expand_dims(x, axis=0)
    preds = model_pneumonia.predict(x)
    return preds

@app.route('/malariadisease', methods=['GET', 'POST'])
def malariadisease():
    if request.method=="GET":
        return render_template('malariadisease.html', title='Malaria Disease')
    else:
        f=request.files["file"]
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(basepath,'uploads',  secure_filename(f.filename))
        f.save(file_path)

        prediction = malaria_predict(file_path)
        if prediction[0][0]>=0.5:
            return render_template('prediction.html', prediction_text="The image indicates the presence of Malaria.", image_name = f.filename, greet="Oops!", title='Malaria Disease')
        else:
            return render_template('prediction.html', prediction_text="The image indicates you don't have Malaria.", image_name= f.filename, greet="Great!", title='Malaria Disease')

@app.route('/pneumoniadisease', methods=['GET', 'POST'])
def pneumoniadisease():
    if request.method=="GET":
        return render_template('pneumoniadisease.html', title='Pneumonia Disease')
    else:
        f=request.files["file"]
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(basepath,'uploads',  secure_filename(f.filename))
        f.save(file_path)

        prediction = pneumonia_predict(file_path)
        pred=np.argmax(prediction, axis=1)
        if pred[0]==1:
            return render_template('prediction.html', prediction_text="This X-Ray shows the presence of Pneumonia.", file_name = f.filename, greet="Oops!", title='Pneumonia Disease')
        else:
            return render_template('prediction.html', prediction_text="This X-Ray shows you don't have Pneumonia.", file_name= f.filename, greet="Great!", title='Pneumonia Disease')


@app.route('/uploads/<filename>')
def send_file(filename):
    return send_from_directory('uploads', filename)

if __name__=='__main__':
	app.run(debug=True)

