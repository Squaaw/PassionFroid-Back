import io, os, base64, math, http.client, urllib.parse, json
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
import environ
import requests

env = environ.Env()
environ.Env.read_env()

# Authentication to Azure Cognitive Services
HOST = os.getenv('AZURE_COGNITIVE_SERVICES_HOST')
ENDPOINT = f'https://{HOST}'
SUBSCRIPTION_KEY = os.getenv('AZURE_COGNITIVE_SERVICES_SUBSCRIPTION_KEY')
API_VERSION_VISION = os.getenv('AZURE_COMPUTER_VISION_API_VERSION')

def describe_image_from_url(image_url):
    computervision_client = ComputerVisionClient(ENDPOINT, CognitiveServicesCredentials(SUBSCRIPTION_KEY))
    describe_image_result = computervision_client.describe_image(image_url)
    return describe_image_result

def describe_image_from_base64(image_base64):
    try:
        base64Split = image_base64.split(',')[1]
        binary_code = base64.b64decode(base64Split)
        image = io.BytesIO(binary_code)
        computervision_client = ComputerVisionClient(ENDPOINT, CognitiveServicesCredentials(SUBSCRIPTION_KEY))
        describe_image_result = computervision_client.describe_image_in_stream(image)

        return describe_image_result
    except Exception as error:
        print(f"Une erreur est survenue lors de l'analyse de l'image : {error}")

def get_image_vector_from_url(image_url):
    request_headers = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': SUBSCRIPTION_KEY,
    }

    request_body = {
        'url': image_url
    }

    try:
        conn = http.client.HTTPSConnection(host=HOST)
        conn.request(method="POST", url=f"/computervision/retrieval:vectorizeImage?api-version={API_VERSION_VISION}&model-version=latest", body=json.dumps(request_body), headers=request_headers)

        response = conn.getresponse()
        data = response.read()
        json_data = json.loads(data)
        image_vector = json_data["vector"]
        conn.close()

        return image_vector
    except:
        raise("An error occured while fetching image's vector")

def get_image_vector_from_base64(image_base64):
    request_headers = {
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': SUBSCRIPTION_KEY,
    }

    url = f"{ENDPOINT}/computervision/retrieval:vectorizeImage?api-version={API_VERSION_VISION}&model-version=latest"
    base64Split = image_base64.split(',')[1]
    binary_code = base64.b64decode(base64Split)
    data = io.BytesIO(binary_code)

    response = requests.post(url=url, data=data, headers=request_headers)

    if response.status_code != 200:
        raise("An error occured while fetching API. Wether the file or the subscription's key is not valid.")
    
    json_data = json.loads(response.content)
    image_vector = json_data["vector"]

    return image_vector

def get_text_vector(text):
    request_headers = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': SUBSCRIPTION_KEY,
    }

    request_body = {
        'text': text
    }

    try:
        conn = http.client.HTTPSConnection(host=HOST)  
        conn.request(method="POST", url=f"/computervision/retrieval:vectorizeText?api-version={API_VERSION_VISION}&model-version=latest", body=json.dumps(request_body), headers=request_headers)
        
        response = conn.getresponse()
        data = response.read()
        json_data = json.loads(data)
        text_vector = json_data["vector"]
        conn.close()

        return text_vector
    
    except:
        raise("An error occured while fetching text's vector")

def get_cosine_similarity(imageVector, textVector):
    dotProduct = 0
    length = min(len(imageVector), len(textVector))

    for i in range(length):
        dotProduct += imageVector[i] * textVector[i]

    magnitude1 = math.sqrt(sum(x * x for x in imageVector))
    magnitude2 = math.sqrt(sum(x * x for x in textVector))

    return dotProduct / (magnitude1 * magnitude2)