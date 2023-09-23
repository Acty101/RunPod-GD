import runpod
import os
import io
import logging
import typing
import base64
import json
import torch
import numpy as np
import cv2 as cv
import time
from groundingdino.util.inference import load_image, predict, annotate, load_model

DEVICE = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
model_path = './weights'

def _predict(model, image_source: np.ndarray, image: torch.Tensor, text_prompt: str):
    BOX_TRESHOLD = 0.35
    TEXT_TRESHOLD = 0.25
    logging.info(f"---> {image.shape}, {DEVICE}")
    boxes, logits, phrases = predict(
        model=model,
        image=image,
        caption=text_prompt,
        box_threshold=BOX_TRESHOLD,
        text_threshold=TEXT_TRESHOLD,
        device=DEVICE,
    )

    annotated_frame = annotate(
        image_source=image_source, boxes=boxes, logits=logits, phrases=phrases
    )

    return annotated_frame, boxes, logits, phrases

def get_model(model_dir):
    return load_model(
        os.path.join(
            os.getenv("GD_CODE_PATH", "."),
            "GroundingDINO/groundingdino/config/GroundingDINO_SwinT_OGC.py",
        ),
        os.path.join(model_dir, "groundingdino_swint_ogc.pth"),
    )

def process_input(body):
    image_b64 = body["image"]
    text = body["text_prompt"]

    buf = io.BytesIO(base64.b64decode(image_b64))

    ori_img_np, transformed_img_tensor = load_image(buf)

    logging.info(f"Loaded image: {ori_img_np.shape}")
    logging.info(f"Loaded transformed image: {transformed_img_tensor.shape}")
    logging.info(f"Using text prompt: {text}")

    return {
        "text_prompt": text,
        "ori_img": ori_img_np,
        "transformed_img": transformed_img_tensor,
    }

def make_prediction(input_object: typing.Dict, model):
    logging.info("Prediction started")
    annotated_frame, boxes, logits, phrases = _predict(
        model,
        input_object["ori_img"],
        input_object["transformed_img"],
        input_object["text_prompt"],
    )

    logging.info(f"{logits}, {phrases}")
    return {"predicted_frame": annotated_frame}

def process_output(prediction: typing.Dict[str, np.ndarray]):
    logging.info("Post-processing..")
    logging.info(prediction)

    is_success, buffer = cv.imencode(".jpg", prediction["predicted_frame"])
    bytes_data = io.BytesIO(buffer).read()
    encoded_string = base64.b64encode(bytes_data)
    return encoded_string.decode("utf-8")



# if testing locally, uncomment below to load data into json file
#####
# from utils import configure_data, generate_file_from_output
# img_path = "./data/samples/mei.jpeg"
# data = configure_data(img_path)
# with open("test_input.json", "w") as j:
#     json.dump(data, j)
#####

# load the model
start = time.time()
model = get_model(model_path)
end = time.time()
logging.info(f"Time taken to load model:{end-start}")

def handler(event):
    body = event["input"]
    processed_input = process_input(body)
    prediction = make_prediction(processed_input, model)
    processed_output = process_output(prediction)
    return processed_output

# start the local serverless instance
runpod.serverless.start({"handler": handler})