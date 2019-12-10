import csv
import math
import cmath
import matplotlib.pyplot as plotter
import numpy as np
from scipy import signal


def butter_bandpass(lowcut, highcut, fs, order=5, label=None):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = signal.butter(order, [low, high], btype='band')
    return b, a


samplingFrequency = 256
samplingInterval = 1 / samplingFrequency

beginTime = 0
endTime = 2
time_quantity = endTime - beginTime

time = np.arange(beginTime, endTime, samplingInterval)

# reading the csv file
file_name = "data.csv"
with open(file_name, "rt") as cfile:
    csv = csv.reader(cfile, delimiter=" ", quotechar="|")
    a_list = []

    for row in csv:
        a_list.append(row[0].split(","))

O1 = []
O2 = []
for i in a_list[1:]:
    O1.append(i[7])
    O2.append(i[8])

OS = [O1, O2]

# Number of columns
m = len(OS)
# Number of rows
n = len(OS[1])

x = [0] * m
k = -1
for i, col in enumerate(OS):
    for j, row in enumerate(col):
        x[i] = x[i] + float(row) * cmath.exp(complex(0.0, -2 * math.pi * i * k / n))

for fft in x:
    print(fft)

# Add the sine waves
amplitude = O1 + O2
length = time_quantity * samplingFrequency
amplitude = amplitude[:length]

# Frequency domain representation
fourierTransform = np.fft.fft(amplitude) / len(amplitude)  # Normalize amplitude
fourierTransform = fourierTransform[range(int(len(amplitude) / 2))]  # Exclude sampling frequency

tpCount = len(amplitude)
values = np.arange(int(tpCount / 2))
timePeriod = tpCount / samplingFrequency
frequencies = values / timePeriod

figure, axis = plotter.subplots(3, 1)
plotter.subplots_adjust(hspace=1)

low = 8
high = 12
filtered, _ = signal.butter(5, [low, high], 'bandpass', analog=True)
print(filtered)
print(fourierTransform)

# Time domain representation of the resultant sine wave
axis[0].set_title('Before fourier')
axis[0].plot(time, amplitude)
axis[0].set_xlabel('Time')
axis[0].set_ylabel('Amplitude')

# Frequency domain representation
axis[1].set_title('After fourier')
axis[1].plot(frequencies, abs(fourierTransform))
axis[1].set_xlabel('Frequency')
axis[1].set_ylabel('Amplitude')

# Frequency domain representation
axis[2].set_title('Filtered')
axis[2].plot(frequencies, abs(filtered))
axis[2].set_xlabel('Frequency')
axis[2].set_ylabel('Amplitude')

plotter.show()
