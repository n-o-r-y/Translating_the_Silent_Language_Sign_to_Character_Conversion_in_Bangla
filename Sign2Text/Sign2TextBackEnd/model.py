import tensorflow as tf
import numpy as np

from loaders import SingletonModelLoader


def transform_array_to_tensor(array, batch_number=1, channel=3):
    # Add batch and channel dimensions to the array
    array_expanded = np.expand_dims(array, axis=(0, -1))
    array_expanded = np.repeat(array_expanded, batch_number, axis=0)
    array_expanded = np.repeat(array_expanded, channel, axis=-1)

    # Convert the array to a TensorFlow tensor
    tensor = tf.convert_to_tensor(array_expanded, dtype=tf.float32)

    return tensor

def get_prediction(image_np_array):

    model_loader = SingletonModelLoader('hybrid_model.pkl')
    model = model_loader.get_model()

    image_tensor_processed = transform_array_to_tensor(image_np_array)

    predicted_value = model.predict(image_tensor_processed)

    return predicted_value
