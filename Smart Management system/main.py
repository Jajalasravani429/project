from fastapi import FastAPI, UploadFile, File
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
from io import BytesIO
from PIL import Image

app = FastAPI()

# Load model once at startup
model = load_model("waste_classifier_model.h5")
class_names = ['N', 'O', 'R']

def read_imagefile(file):
    img = Image.open(BytesIO(file))
    return img

@app.post("/predict")
def predict(file: UploadFile = File(...)):
    img = read_imagefile(file.file.read())
    img = img.resize((224, 224))
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    
    prediction = model.predict(img_array)
    predicted_class = class_names[np.argmax(prediction)]

    return {"class": predicted_class}
