# Import the necessary libraries
from sense_hat import SenseHat
from time import sleep
from datetime import datetime
import sys
import os
from google.cloud import firestore

# Constants
COLLECTION_NAME = u'pis'
PI_ID = u'stc_pi_1'

# Variables
temperature = 0
humidity = 0
pressure = 0

# Make an instance of SenseHat
sense = SenseHat()
sense.set_imu_config(False, False, False)
# Clear the RGB matrix
sense.clear()

# Initalize Firebase
# Use the service account for own server
os.chdir(os.path.dirname(__file__))
dirpath = os.getcwd()
db = firestore.Client.from_service_account_json(dirpath + '/config/start-to-code-70340204ea7b.json')

# function: on_snapshot(doc_snapshot, changes, read_time)
def celcius_to_farenheit(celsius):
    return ((celsius/5*9)+32)

# function: get_cpu_temp()
# get the real temperature
def get_real_temp():
    res = os.popen('python3 temperature_real.py False').readline()
    t = float(res.replace('temp=', '').replace("C\n", ''))
    return(t)

# Get the pi environment ref
pi_ref = db.collection(COLLECTION_NAME).document(PI_ID)

while True:
    try:
        temperature_next = round(get_real_temp(),1)
        sleep(2)

        if temperature_next != temperature:
            environmentObj = {
                u'temperature': {
                    u'value': temperature_next,
                    u'unit_code': u'°C',
                    u'unit_text': u'Celsius'
                },
                
            }
            pi_ref.set({ 'environment': environmentObj }, merge=True )
            temperature = temperature_next
            

        sleep(60)

    except (KeyboardInterrupt, SystemExit):
        print('Interrupt received! Stopping the application...')
        sense.clear()
        sys.exit(0)