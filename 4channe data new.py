import nidaqmx
from nidaqmx.constants import AcquisitionType
import numpy as np
import matplotlib.pyplot as plt
import datetime

filename = datetime.datetime.now()
fig, axs = plt.subplots(2, 2)
sample_time = 2  # units = seconds
s_freq = 10000
num_samples = sample_time*s_freq
dt = 1/s_freq

with nidaqmx.Task() as task:
   
   ## task.ai_channels.add_ai_voltage_chan("Dev1/ai0:3", terminal_config=nidaqmx.constants.TerminalConfiguration.RSE, min_val=0.0, max_val=5.0)
    task.ai_channels.add_ai_voltage_chan("Dev1/ai0:3", min_val= -10.0, max_val=10.0)
    task.timing.cfg_samp_clk_timing(s_freq,sample_mode = AcquisitionType.FINITE,samps_per_chan=num_samples)
    system= nidaqmx.system.System.local()
    print("start")
    data = task.read(number_of_samples_per_channel=num_samples, timeout = nidaqmx.constants.WAIT_INFINITELY)  #data is a 100000*4 array
    a0=data[0][:]
    a1=data[1][:]
    a2=data[2][:]
    a3=data[3][:]
    axs[0, 0].plot(a0,linewidth=0.5)
    axs[0, 0].set_title('UL:QPD[0,0]')
    axs[0, 1].plot(a1, 'tab:orange',linewidth=0.5)
    axs[0, 1].set_title('UR:QPD[0,1]')
    axs[1, 0].plot(a3, 'tab:green',linewidth=0.5)
    axs[1, 0].set_title('DL:QPD[1,0]')
    axs[1, 1].plot(a2, 'tab:red',linewidth=0.5)
    axs[1, 1].set_title('DR:QPD[1,1]')
    #plt.tight_layout()
    #plt.savefig(filename.strftime("%Y_%b_%d__%H_%M_%S")+'.png',dpi=1200,bbox_inches='tight')
    plt.show()
    y =  np.transpose(data)
    np.savetxt(filename.strftime("%Y_%b_%d__%H_%M_%S")+".txt", y ,fmt="%s",delimiter=",")
    plt.close()
    n = len(a0) # total number of samples
    T=n*0.0001  # Sample Period
    t = np.linspace(0, T, n)
    A0=np.array(a0)
    A1=np.array(a1)
    A2=np.array(a2)
    A3=np.array(a3)   
    plt.plot(t,-(A0-np.mean(A0)),'r',t,-(A1-np.mean(A1)),'g',t,-(A2-np.mean(A2)),'b',t,-(A3-np.mean(A3)),'y',linewidth=0.9)
    plt.show()
