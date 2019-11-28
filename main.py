import asyncio
import json
from lib.cortex import Cortex

async def do_stuff(cortex):
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
            
            data_json = await cortex.get_data()
            data = json.loads(data_json)
            F8_data = data['eeg'][14]

            if F8_data < threshold:
                if previous_low is False:
                    previous_low = True
                    print(f"GOING LOOOOW : {F8_data}" )
            else:
                if previous_low is True:
                    previous_low = False
                    print(f"GOING HIGHHHH : {F8_data}")

        await cortex.close_session()

def main():
    cortex = Cortex('./cortex_creds')
    asyncio.run(do_stuff(cortex))
    cortex.close()

if __name__ == '__main__':
    main()