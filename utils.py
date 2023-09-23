import base64
import io
from PIL import Image

URL = "https://api.runpod.ai/v2/64t3ke7ey4inh3"

def image_to_base64(filepath):
    with open(filepath, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
        return encoded_string.decode("utf-8")

def bytes_to_image(byte_data):
    image_stream = io.BytesIO(byte_data)
    image = Image.open(image_stream)
    return image

def configure_data(img_path):
    img_b64 = image_to_base64(img_path)
    return {"input": {
        "image": img_b64, 
        "text_prompt": "person"
        }
    }

def generate_file_from_output(output, filename):
    imgdata = base64.b64decode(output)
    with open(filename, 'wb') as f:
        f.write(imgdata)