from google.cloud import storage
import time
from CLASSML.params import *
import pickle

# def save_model(model):
#     timestamp = time.strftime("%Y%m%d-%H%M%S")
#     model_filename = f'{timestamp}.h5'

#     client=storage.Client()
#     bucket=client.bucket(BUCKET_NAME)
#     blob=bucket.blob(f"models/{model_filename}")
#     blob.upload_from_filename(model_path)

def load_model_scale():
    client = storage.Client()
    blobs = list(client.get_bucket(BUCKET_NAME).list_blobs(prefix="classifier"))

    model_path_to_save = os.path.join(LOCAL_REGISTRY_PATH, blobs[0].name)
    blobs[0].download_to_filename(model_path_to_save)

    with open(model_path_to_save, 'rb') as file:
        model = pickle.load(file)

    print("✅ classifier model downloaded from cloud storage")
    return model

def load_linear_model():
    client=storage.Client()
    blobs= list(client.get_bucket(BUCKET_NAME).list_blobs(prefix='linear'))

    model_path_to_save=os.path.join(LOCAL_REGISTRY_PATH,blobs[0].name)
    blobs[0].download_to_filename(model_path_to_save)

    with open(model_path_to_save,'rb') as file:
        model=pickle.load(file)
    print('✅ linear model downloaded from cloud storage')
    return model
