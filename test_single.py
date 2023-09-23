import os
import time

from utils import URL, configure_data, generate_file_from_output

def main():
    import requests
    from dotenv import load_dotenv
    load_dotenv()
    img = "./data/samples/single-person.jpeg"
    payload = configure_data(img)

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": os.getenv('RUNPOD_API_KEY')
    }

    response = requests.post(os.path.join(URL, 'run'), json=payload, headers=headers)
    response = response.json()
    print(response)
    STATUS = response['status']
    result_url = os.path.join(URL, 'status', response['id'])
    print(result_url)
    while(STATUS == "IN_QUEUE" or STATUS == "IN_PROGRESS"):
        # wait awhile and update
        print("waiting for response...")
        time.sleep(5)
        response = requests.get(result_url, headers=headers)
        response = response.json()
        STATUS = response['status']

    print("Not in queue anymore")

    if(STATUS == "COMPLETED"):
        print("Output received!")
        print(f"delay: {response['delayTime']}")
        print(f"execution: {response['executionTime']}")
        generate_file_from_output(response['output'], f"./data/output/{img.split('/')[-1]}")
        print("Image file generated")
        print()
    else:
        print("Couldn't receive output")
        print("Response:", response)

if __name__ == "__main__":
    main()


