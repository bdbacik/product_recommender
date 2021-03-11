import pandas as pd
import scipy
import scipy.sparse as sps
import implicit
import numpy as np
from time import perf_counter as pc
import json
from train import *



df = '/Users/Brian/Dropbox/drizly/recommendations_take_home.csv'

start_time = pc()
content_engine.train(df)
end_time = pc()
print('time: ', end_time-start_time)



request_id = '0a992174178e8303dcfffadef857c776'
recos = content_engine.predict(request_id)
print(recos)