import argparse
import dotenv
import os
import requests
import shutil

parser = argparse.ArgumentParser()
parser.add_argument("--plant", type=str, help="Name of a flower or plant")
args = parser.parse_args()

#step1: post teh name of flower or planet to illusion diffsion to make an image of it

url = "https://fal.run/fal-ai/illusion-diffusion"
dotenv.load_dotenv()
Fal_API_key = os.getenv("Fal_API_key")
headers = {
    "Authorization": Fal_API_key,
    "Content-Type": "application/json"
}

payload = {
    "image_url": "https://storage.googleapis.com/falserverless/illusion-examples/checkers.png",
    "prompt": f"(masterpiece:1.4), (best quality), (detailed),(just one plant with no extra flower or tree), {args.plant}",
    "negative_prompt": "(worst quality, poor details:1.4), lowres, (artist name, signature, watermark:1.4), bad-artist-anime, bad_prompt_version2, bad-hands-5, ng_deepnegative_v1_75t"

}

response = requests.post(url, headers=headers, json=payload)
try:
    response_json=response.json()
except:
    print(f"https://fal.run/fal-ai/illusion-diffusion server response is {response.status_code}")


response = requests.get(response_json['image']['url'], stream = True)

if response.status_code == 200:
    with open('assets/image.jpg','wb') as f:
        shutil.copyfileobj(response.raw, f)
    print('Image sucessfully downloaded and saved in the assets folder.')



#step2: post the image of flower or plant to plantnet to recognise it
    
url = "https://my-api.plantnet.org/v2/identify/all"
dotenv.load_dotenv()
PlantNet_API_key = os.getenv("PlantNet_API_key")
headers = {}
payload = {
    "api-key": PlantNet_API_key
}
files = {
    "images": open("assets/image.jpg", "rb")
}
try:
    response = requests.post(url, headers=headers, params=payload, files=files)
    print(response.json()['commonNames'][0])
except:
    print(f"https://my-api.plantnet.org server response is {response.status_code}")