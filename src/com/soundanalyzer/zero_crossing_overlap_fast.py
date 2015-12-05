import numpy
import matplotlib.pyplot as plt
from scipy.signal.filter_design import butter, buttord
from scipy.signal import lfilter, lfiltic
import scipy.io.wavfile
from scipy import signal

print "Enter file name\n"
file_name = raw_input()

print "Enter center frequency\n"
base_freq = int(raw_input())

print "Reading file.....\n"
fs,mysignal=scipy.io.wavfile.read(file_name)
print "File read\n"
refined_signal = numpy.float64(mysignal / 32768.0)
# fs=sampling frequency,signal is the numpy 2D array where the data of the wav file is written
length=len(mysignal)
duration = float(length / (1.0*fs))
original = mysignal
dt = float (duration/((length-1)*1.0))
dt = 0.000125    #1/fs
dt = float(1.0/fs)
curtime = 0.0
time_line = []
for i in range(length):
    time_line.append(curtime)
    curtime = curtime + dt
    
filtered = numpy.int32(refined_signal*32768)

mysignal = filtered
#mysignal.lstrip(0.0)
#mysignal.rstrip(0.0)

T = len(mysignal)
Amp = mysignal
freq = []
win_size = 1000

print T,1000,T*1000

print "begin\n"

for i in range(T-1):
    print "currently at "+str(i)+" to go = "+str(T-i)
    if (i+win_size)>T-1:
        break
    else:
        X = []
        for j in range(i,i+win_size):
            '''if Amp[j]==0:
                x = float(j)
                x = x*dt
                X.append(x)
            else:'''
            if ((Amp[j]*Amp[j+1])<=0):
                if Amp[j+1]==0 and j+1!=(i+win_size-1):
                    continue
                dx = dt
                dy = float(Amp[j+1] - Amp[j])
                m = float(dy/dx)
                c = float(Amp[j] - (m*j*dt))
                x = float((c/(m+0.00000000000001))*(-1.0))
                X.append(x)
        
        avg_delta_T = 0.0
        for k in range(1,len(X)):
            deltaT = 2*(X[k] - X[k-1])
            avg_delta_T += deltaT 
        
        print "avg delta, number of zero crossings : "+str(avg_delta_T)+" , "+str(len(X))
        print "in cur win_ zero points = "+str(len(X))
        if (len(X)<=1):
            continue
        avg_delta_T = float(avg_delta_T/((1.0)*(len(X)-1)))
        data = 1.0/(avg_delta_T+0.000000000000001)
        freq.append(data)   
        #print data
 
print "end\n"
       
final = []
tstamp = []
BASE = base_freq
f_low = BASE - float((10/100.0)*(BASE)) 
f_high = BASE + float((10/100.0)*(BASE))
for i in range(len(freq)):
    f = freq[i]
    if ((f<=f_high) and (f>=f_low)):
        final.append(f)
        tstamp.append(i)
        
print len(final)
if len(final)>100:
    plt.figure(2)
    plt.clf()
    plt.plot(final,"ro",label="frequency by averaging")
    plt.legend()
    plt.show()

else :
    print "Not enough points in BASE range"
    
Avg_freq = []
window_ = len(final)/1000
id_ = 0 
while id_<len(final):
    if id_+window_>=len(final):
        break
    avg = 0.0
    for i in range(id_,id_+window_):
        avg += final[i]
    
    data = avg/window_
    Avg_freq.append(data)
    id_ = id_ + window_    
    
if len(Avg_freq)>100:
    plt.figure(3)
    plt.clf()
    plt.plot(Avg_freq,label="frequency by averaging")
    plt.legend()
    plt.show()

else :
    print "Not enough points in BASE range" 
        

