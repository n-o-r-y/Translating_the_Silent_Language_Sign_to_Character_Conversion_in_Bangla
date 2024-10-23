import cv2
import numpy as np
import base64
from io import BytesIO
from PIL import Image
from rembg import remove

from loaders import SingletonSessionLoader


GAMMA = 1.5
RESIZE_DIMENSIONS = (256, 256)

def get_background_removed_image(image):
    model_name = "u2net"

    session_loader = SingletonSessionLoader(model_name=model_name)
    rembg_session = session_loader.get_session()

    output = remove(
        image,
        session=rembg_session,
        alpha_matting=True,
        alpha_matting_foreground_threshold=270,
        alpha_matting_background_threshold=20,
        alpha_matting_erode_size=11,
    )

    return output

def gamma_correction(image, gamma=1.0):
    inv_gamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** inv_gamma) * 255.0 for i in np.arange(0, 256)]).astype("uint8")
    return cv2.LUT(image, table)

def get_base64_from_np_array_image(image):
    image_object = Image.fromarray(image)

    image_file = BytesIO()
    image_object.save(image_file, format="PNG")
    image_bytes = image_file.getvalue()

    image_base64 = base64.b64encode(image_bytes).decode("utf-8")

    return image_base64

def get_preprocessed_image(image_str):
    background_removed_image = get_background_removed_image(image_str)

    image_bytes = np.frombuffer(background_removed_image, np.uint8)
    image = cv2.imdecode(image_bytes, cv2.IMREAD_COLOR)

    resized_image = cv2.resize(image, RESIZE_DIMENSIONS)
    gray_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)
    enhanced_image = cv2.equalizeHist(gray_image)

    gamma_corrected_image = gamma_correction(enhanced_image, gamma=GAMMA)

    base_64_image_str = get_base64_from_np_array_image(gamma_corrected_image)

    return base_64_image_str, gamma_corrected_image
