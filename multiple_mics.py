import pyaudio as pyaudio
import numpy as np
import pandas as pd
from datetime import datetime
import time
import matplotlib.pyplot as plt

# initiallizes data structure to hold data
frames = bytearray()
frames2 = bytearray()

# Sampling parameters
CHUNK = 1024 # parameter related to the data buffer
samplerate = 44100 # samples per second
sampletime = 45 # seconds
index1 = 1 # device index of the first microphone
index2 = 3 # device index of the second microphone
dist=39.5 # inches


s=pyaudio.PyAudio()

# This block lists the audio devices on the computer.
# alldevicecount = s.get_device_count()
#for deviceindex in range(alldevicecount):
#   devnow = s.get_device_info_by_index(deviceindex)
#   if devnow.get("maxInputChannels") > 0:
#      print(str(deviceindex) + ": " + str(devnow))

p = pyaudio.PyAudio()
p2 = pyaudio.PyAudio()

# Open the first recording data stream.
stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=samplerate,
                input=True,
                frames_per_buffer=CHUNK,
                input_device_index=index1)

# Open the second recording data stream.
stream2 = p2.open(format=pyaudio.paInt16,
                channels=1,
                rate=samplerate,
                input=True,
                frames_per_buffer=CHUNK,
                input_device_index=index2)

print("I'm recording!!")

# Get the start time in seconds from 1970. This is used to time the loop. 
start_timestamp = time.time()
continueloop = True
while continueloop:
    data = stream.read(CHUNK) 
    data2 = stream2.read(CHUNK)   
    frames.extend(data)
    frames2.extend(data2)

    loop_timestamp = time.time()
    continueloop = (loop_timestamp - start_timestamp < sampletime) # this line will turn false when the recording time is complete and fall out of the loop.

# Stop recording and close the streams.
stream.stop_stream()
stream.close()
p.terminate()

stream2.stop_stream()
stream2.close()
p2.terminate()

# Data formatting
frames = bytes(frames)
frames2 = bytes(frames2)

amplitude = np.frombuffer(frames, np.int16)
amplitude2 = np.frombuffer(frames2, np.int16)

amplitude = np.transpose(amplitude)
amplitude2 = np.transpose(amplitude2)

# Save to disk
print("Done recording - saving to disk")

filepath = '.\\data\\'
filenameprefix = 'data_d='+str(dist)+'_'

# getting the current date and time
current_datetime = datetime.now()

# getting the date and time from the current date and time in the given format
filenamesuffix = current_datetime.strftime("%Y%m%d%H%M%S")
fullfilename = filepath+filenameprefix+filenamesuffix+'.csv'

# format the data for saving in a csv table. Create the time column.
times = pd.DataFrame(np.linspace(0, sampletime, amplitude.shape[0]))
times.columns = ["Time (s)"]

# Create the sound data columns.
sounddata = pd.DataFrame(amplitude)
sounddata2 = pd.DataFrame(amplitude2)

# Stick the columns together.
fulldata = pd.concat([times,sounddata,sounddata2],axis = 1)

fulldata.columns = ["Time (s)", "Mic 1", "Mic 2"]
 
 # Save to file. 
fulldata.to_csv(fullfilename)

# Plot the data for initial confirmation.
print("Plotting...")
fig, ax = plt.subplots()
lines = ax.plot(fulldata["Time (s)"],fulldata["Mic 1"],'r',fulldata["Time (s)"], fulldata["Mic 2"], 'b')
ax.legend(["Channel 1", "Channel 2"],
           loc='lower left', ncol=2)

ax.yaxis.grid(True)

fig.tight_layout(pad=0)
plt.show()

print("Done!")

