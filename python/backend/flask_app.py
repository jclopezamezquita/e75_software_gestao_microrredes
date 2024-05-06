import re
from api_tools.db import db
from api_tools.app import create_app
import cron_tools.cron_functions as cron_functions
from flask_migrate import Migrate
from uwsgidecorators import *
import time
from datetime import datetime
import os
from flask_cors import CORS
import random
import math
from flask import jsonify


# Contruction of the API and the the database tables
app = create_app()
migrate = Migrate(app, db)
CORS(app, resources={r'/*': {'origins': '*'}})


# create the DB on demand
@app.before_first_request
def create_DB():
    db.create_all()

# uwsgidecorators.timer(interval, func)
@timer(60)
def leitura_medidas_laboratoriais(num):
    '''
    This cron is executed every one minutes
    '''
    now = datetime.now()
    print ("%s/%s/%s %s:%s:%s" % (now.month,now.day,now.year,now.hour,now.minute,now.second))
    
    #resultado = cron_functions.microgrid_measurements(URL=os.getenv('HIL_API_URL', 'https://ems-api.ngrok.io/'))
    resultado = cron_functions.microgrid_measurements(URL='http://100.112.150.188:5000/')


# uwsgidecorators.cron(min, hour, day, mon, wday, func) -> BST: UTC-3
@cron(54, 2, -1, -1, -1)
def cron_everyday(num):
    '''
    This cron is executed every day at the end of the day - dispatch defined for the next day
    '''
    start = time.time()
    resultado = cron_functions.microgrid_dayahead_optimizer()
    if resultado:
        cron_functions.write_results_database(resultado)
    end = time.time()

    print("The time of execution of EDO is: ", (end-start), "s")

    resultado2 = cron_functions.delete_old_measurements(timezone_SP=3)

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)