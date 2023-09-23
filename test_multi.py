from utils import URL, configure_data, generate_file_from_output
import requests
import os
import time
from dotenv import load_dotenv

def main():
    input_img_folder = './data/samples'
    output_img_folder = './data/output'
    load_dotenv()
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": os.getenv('RUNPOD_API_KEY')
    }
    files = os.listdir(input_img_folder)

    for file in files:
        img = os.path.join(input_img_folder, file)
        payload = configure_data(img)
        response = requests.post(os.path.join(URL, 'run'), json=payload, headers=headers)
        response = response.json()
        print(response)
        STATUS = response['status']
        result_url = os.path.join(URL, 'status', response['id'])
        print(result_url)
        while(STATUS == "IN_QUEUE" or STATUS == "IN_PROGRESS"):
            # wait awhile and update
            print("waiting for response...")
            time.sleep(3)
            response = requests.get(result_url, headers=headers)
            response = response.json()
            STATUS = response['status']

        print("Not in queue anymore")

        if(STATUS == "COMPLETED"):
            print("Output received!")
            print(f"file: {file}")
            print(f"delay: {response['delayTime']}")
            print(f"execution: {response['executionTime']}")
            generate_file_from_output(response['output'], os.path.join(output_img_folder, file))
            print("Image file generated")
        else:
            print("Couldn't receive output")
            print("Response:", response)
    

if __name__ == "__main__":
    main()