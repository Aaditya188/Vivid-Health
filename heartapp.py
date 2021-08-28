# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from flask import Flask, render_template, request
import jsonify
import requests
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler
app = Flask(__name__)
model = pickle.load(open('heartdisease.pkl', 'rb'))
@app.route('/',methods=['GET'])
def Home():
    return render_template('heartdisease.html')

standard_to = StandardScaler()
@app.route("/predict", methods=['POST'])
def predict():
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
    prediction=model.predict([[Age, Gender, ChestPain, BloodPressure, ElectrocardiographicResults, MaxHeartRate, ExerciseInducedAngina, STdepression, ExercisePeakSlope, MajorVesselsNo, Thalassemia]])
    if prediction==1:
        return render_template('heartdisease.html', prediction_text="Oops! The predicted value is [1]. The person seems to have Heart Disease.")
    else:
        return render_template('heartdisease.html', prediction_text="Great! The predicted value is [0]. The person does not have any Heart Disease.")

if __name__=="__main__":
    app.run(debug=True)
