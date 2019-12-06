import asyncio
import json
from lib.cortex import Cortex
import PySimpleGUI as gui

def initWindow():
    gui.change_look_and_feel('DarkGrey')
    # All the stuff inside your window.

    text_component = gui.Text('this is some text', key='__TEXT__')

    layout = [ [gui.Text('emotiv-lightSwitch project :')], [text_component]]
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
    
        print("** SUBSCRIBE EEG **")
        await cortex.subscribe(['eeg'])

        threshold = 4200
        previous_low = False

        # while cortex.packet_count < 10:
        while True:
            
            window.Read(timeout=0)

            data_json = await cortex.get_data()
            data = json.loads(data_json)
            F8_data = data['eeg'][14]

            if F8_data < threshold:
                if previous_low is False:
                    previous_low = True
                    window.Element('__TEXT__').Update('LOW')
                    print(f"GOING LOOOOW : {F8_data}" )
            else:
                if previous_low is True:
                    previous_low = False
                    window.Element('__TEXT__').Update('HIGH')
                    print(f"GOING HIGHHHH : {F8_data}")

        await cortex.close_session()

def main():
    w = initWindow()
    cortex = Cortex('./cortex_creds')
    asyncio.run(do_stuff(cortex, w))
    cortex.close()
    w.close()

if __name__ == '__main__':
    main()