import os
import base64
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials

# Authentication to Azure Cognitive Services
subscription_key = "429c8f33aee34845a441f6920b07f73a"
endpoint = "https://passionfroid-cognitive-services.cognitiveservices.azure.com/"

computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

#########################################
# Call API to analyze an image from URL #
#########################################

remote_image_url = "https://passionfroidstorage.blob.core.windows.net/passionfroid-storage-container/gastronomie-francaise.jpg"
describe_image_result = computervision_client.describe_image(remote_image_url)

############################################
# Call API to analyze an image from base64 #
############################################

# # Get images folder
# images_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images")

# # Get image to convert to base64 (A REMPLACER PAR LE PARAMETRE RECU EN BASE64)
# local_image_path = os.path.join(images_folder, "gastronomie-chef.jpg")

# # Get image's base64
# with open(local_image_path, "rb") as image_file:
#     encoded_string = base64.b64encode(image_file.read())

# # Create image file from base64
# local_image_path = os.path.join(images_folder, "image")

# # Convert base64 to image
# with open(local_image_path, 'wb') as f:
#     f.write(base64.b64decode(encoded_string))

# # Analyze created image from base64
# local_image = open(local_image_path, "rb")
# describe_image_result = computervision_client.describe_image_in_stream(local_image)

# local_image.close()
# os.remove(local_image_path)

# Get image's description
for caption in describe_image_result.captions:
    print(caption.text)

# Get image's tags
for tag in describe_image_result.tags:
    print(tag)