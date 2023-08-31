from .serializers import ImageSerializer
from .models import Image

def get_images_from_db(userId):
    images = Image.objects.filter(user = userId)
    return images
        