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
model = pickle.load(open('breastcancer.pkl', 'rb'))
@app.route('/',methods=['GET'])
def Home():
    return render_template('cancer.html')

standard_to = StandardScaler()
@app.route("/predict", methods=['POST'])
def predict():
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
    prediction=model.predict([[texture_mean, perimeter_mean, smoothness_mean, compactness_mean,
       concavity_mean, concave_points_mean, symmetry_mean, radius_se,
       compactness_se, concavity_se, concave_points_se, texture_worst,
       smoothness_worst, compactness_worst, concavity_worst,
       concave_points_worst, symmetry_worst, fractal_dimension_worst]])
    if prediction==1:
        return render_template('cancer.html', prediction_text="Oops! The tumor is malignant.")
    else:
        return render_template('cancer.html', prediction_text="Great! The tumor is benign.")

if __name__=="__main__":
    app.run(debug=True)
