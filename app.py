import json
from flask import Flask, request, jsonify
import pandas as pd
import os
from os import listdir
import scipy
import scipy.sparse as sps
import implicit
import numpy as np
from models.train import *

app = Flask(__name__)

if __name__ == "__main__":
  app.run(host ='0.0.0.0')


@app.route('/')
def hello_world():
  return 'Hello, Docker!'


#generate predictions for an input user id
@app.route('/reco', methods=['GET','POST'])
def predict() :
  
  #get request data with user id
  content = request.json
  request_id = content['user_id_hash']
  #get top 10 recommendations for user id
  recos = content_engine.predict(request_id)
  return recos

#train the model
@app.route('/train')
def train():

  #train model
  content_engine.train('/data/take_home.csv')
  return 'training complete!'
