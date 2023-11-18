import sounddevice as sd
import numpy as np
import pandas as pd
from datetime import datetime

fs=44100
duration = 3  # seconds
myrecording = sd.rec(duration * fs, samplerate=fs, channels=2,dtype='float64')
print("Recording Audio")
sd.wait()
print("Done recording - saving to disk")

filepath = 'c:\\users\\jaubi\\desktop\\data\\'

filenameprefix = 'data_'

# getting the current date and time
current_datetime = datetime.now()
# getting the date and time from the current date and time in the given format
filenamesuffix = current_datetime.strftime("%Y%m%d%H%M%S")
fullfilename = filepath+filenameprefix+filenamesuffix+'.csv'

times = pd.DataFrame(np.linspace(0, duration, fs*duration))
times.columns = ["Time (s)"]

sounddata = pd.DataFrame(myrecording)

fulldata = pd.concat([times,sounddata],axis = 1)

fulldata.to_csv(fullfilename)

print(fulldata)
print("Done!")