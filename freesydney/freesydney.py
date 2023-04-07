from .imports import *


def download_model_orig(model_name:str=DEFAULT_MODEL, force:bool=False):
    model_fn = model_name+'.bin'
    model_fnfn = os.path.join(PATH_DATA, model_fn)
    model_url = MODEL_URLS.get(model_name)
    if model_url:
        if force or not os.path.exists(model_fnfn):
            print(f'Downloading {model_name} to:\n\n{model_fnfn}\n\nIf you already have a file, please a symbolic link to it from that location.\n')
            download(model_url, model_fnfn)
    return model_fnfn

def download_tokenizer_orig(force:bool=False):
    if force or not os.path.exists(TOKENIZER_PATH):
        download(TOKENIZER_URL,TOKENIZER_PATH)
    return TOKENIZER_PATH

def convert_model_orig(model_name:str=DEFAULT_MODEL, force:bool=False, exec_name:str='pyllamacpp-convert-gpt4all'):
    model_fn = download_model_orig(model_name)
    tokenizer_fn = download_tokenizer_orig()
    newmodel_fn = os.path.splitext(model_fn)[0] + '.ggml' + os.path.splitext(model_fn)[1]
    if force or not os.path.exists(newmodel_fn):
        cmd=f'{exec_name} {model_fn} {tokenizer_fn} {newmodel_fn}'
        print('>>',cmd)
        os.system(cmd)
    return newmodel_fn

def download_converted_model(model_name:str=DEFAULT_MODEL, force:bool=False):
    pass