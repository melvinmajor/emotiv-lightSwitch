import asyncio
import json
from lib.cortex import Cortex
import PySimpleGUI as gui
import numpy as np
import matplotlib.pyplot as plotter
import scipy
import scipy.fftpack
import pylab
from scipy import pi

def initWindow():
    gui.change_look_and_feel('DarkGrey')
    # All the stuff inside your window.

    text_component = gui.Text('this is some text', key='__TEXT__')

    layout = [ [gui.Text('Relaxation level')], [text_component]]
    # Create the window
    window = gui.Window('Preview', layout)
    return window

async def do_stuff(cortex, window):
    # await cortex.inspectApi()
    print("** USER LOGIN **")
    await cortex.get_user_login()
    print("** GET CORTEX INFO **")
    await cortex.get_cortex_info()
    print("** HAS ACCESS RIGHT **")
    await cortex.has_access_right()
    print("** REQUEST ACCESS **")
    await cortex.request_access()
    print("** AUTHORIZE **")
    await cortex.authorize()
    print("** GET LICENSE INFO **")
    await cortex.get_license_info()
    print("** QUERY HEADSETS **")
    await cortex.query_headsets()

    if len(cortex.headsets) > 0:

        print("** CREATE SESSION **")
        await cortex.create_session(activate=True, headset_id=cortex.headsets[0])
    
        print("** SUBSCRIBE POW **")
        await cortex.subscribe(['eeg'])

        max = 0
        min = -1
        level = 1
        sampling_rate = 128
        # sampling_rate = 128
        sampling_frequency = 1 / sampling_rate

        signal = []

        # while cortex.packet_count < 10:
        while True:
            
            if len(signal) >= sampling_rate:
                break

            # window.Read(timeout=0)

            data_json = await cortex.get_data()
            data = json.loads(data_json)['eeg']
            signal.append(data[2])
           
            # window.Element('__TEXT__').Update(f'Level: {signal}')
        
        print(str(len(signal)))
        print(signal)

        fourierTransform = np.fft.fft(signal)/len(signal)
        fourierTransform = fourierTransform[range(int(len(signal)/2))]
        print(fourierTransform)
        print(len(fourierTransform))

        fft = abs(scipy.fft(signal))
        freqs = scipy.fftpack.fftfreq(len(signal), signal[1] - signal[0])
        

        pylab.plot(freqs, 20 * scipy.log10(FFT), 'x')
        pylab.show()

        y = fourierTransform
        x = range(1, len(fourierTransform) + 1)
        #plotter.scatter(x, y)
        #plotter.show()

        await cortex.close_session()

def main():
    # w = initWindow()
    w = 0
    cortex = Cortex('./cortex_creds')
    asyncio.run(do_stuff(cortex, w))
    # cortex.close()
    # w.close()

if __name__ == '__main__':
    main()