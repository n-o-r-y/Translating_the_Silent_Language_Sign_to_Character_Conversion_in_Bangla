import base64
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from model import get_prediction
from preprocess import get_preprocessed_image
from labels import get_label
from loaders import SingletonModelLoader, SingletonSessionLoader


BASE_64_TEXT = 'base64,'

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/initialize")
async def initialize(request: Request):
    print("Request recieved for initialize.")

    try:
        rembg_model_name = 'u2net'
        trained_model_path = 'trained_models/hybrid_model.pkl'

        SingletonModelLoader(file_path=trained_model_path)
        SingletonSessionLoader(model_name=rembg_model_name)

        return JSONResponse(
            content={'message': 'Model initialized.'},
            status_code=200
        )
    except Exception as e:
        return JSONResponse(
            content={'message': f"Something went wrong. This is what we know: ${e}"},
            status_code=400
        )

@app.post("/get_prediction")
async def predict(request: Request):
    try:
        data = await request.json()
        image_data = data['image']

        split_index = image_data.index(BASE_64_TEXT) + len(BASE_64_TEXT)

        info_string = image_data[:split_index]
        base64_string = image_data[split_index:]

        image_bytes = base64.b64decode(base64_string)

        preprocessed_image, image_np_array = get_preprocessed_image(image_bytes)
        prediction_result = get_prediction(image_np_array)

        most_probable_value_index = prediction_result.argmax(axis=1)[0]

        label = get_label(most_probable_value_index)

        return JSONResponse(
            content={
                'preprocessed_image': str(info_string + preprocessed_image),
                'letter': label
            },
            status_code=200
        )
    except Exception as e:
        return JSONResponse(
            content={'message': f"Something went wrong. This is what we know: ${e}"},
            status_code=400
        )
