from flask import Flask, render_template, request, redirect, url_for, session
import numpy as np
import pandas as pd
import joblib
from Model import LLM
from ModelPipeline import Aspect


app = Flask(__name__, template_folder='template')

# Home page that displays the input form
@app.route('/')
def home():
    return render_template('home2.html')

@app.route('/home2', methods=['POST'])
def output():
    text = 'Enter Review'

    # Get the data from the input form
    if request.method == 'POST':
        user_input = request.form['user_input']


        # # loading model
        # model_instance = joblib.load('modeldump.pkl')
        model_instance = LLM()

        # # model instance and prediction
        model = Aspect(model_instance)
        prediction = model.predict(user_input)
        user_input = prediction


        return render_template('home2.html', user_input = user_input)
    return render_template('output.html', text = text)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port='8080')
    #app.run()