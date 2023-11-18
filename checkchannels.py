import pyaudio as pyaudio

s=pyaudio.PyAudio()

# This block lists the audio devices on the computer.
alldevicecount = s.get_device_count()
for deviceindex in range(alldevicecount):
   devnow = s.get_device_info_by_index(deviceindex)
   if devnow.get("maxInputChannels") > 0:
      print(str(deviceindex) + ": " + str(devnow))