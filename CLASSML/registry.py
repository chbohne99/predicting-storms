from google.cloud import storage
import time


def save_model(model):
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    model_filename = f'{timestamp}.h5'

    client=storage.Client()
    bucket=client.
