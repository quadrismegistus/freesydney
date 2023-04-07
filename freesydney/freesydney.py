from .imports import *


def download_model(model_name:str=DEFAULT_MODEL, force:bool=False):
    model_url = MODEL_URLS.get(model_name)
    if model_url:
        model_fn = model_name+'.bin'
        model_fnfn = os.path.join(PATH_DATA, model_fn)
        if force or not os.path.exists(model_fnfn):
            print(f'Downloading {model_name} to:\n\n{model_fnfn}\n\nIf you already have a file, please a symbolic link to it from that location.\n')
            download(model_url, model_fnfn)

            