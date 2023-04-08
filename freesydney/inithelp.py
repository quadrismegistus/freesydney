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
    newmodel_fn = os.path.join(PATH_DATA, model_name+'.ggml.bin')
    if force or not os.path.exists(newmodel_fn):
        model_fn = download_model_orig(model_name)
        tokenizer_fn = download_tokenizer_orig()    
        cmd=f'{exec_name} {model_fn} {tokenizer_fn} {newmodel_fn}'
        print('>>',cmd)
        os.system(cmd)
    return newmodel_fn

def convert_unfiltered_model(): convert_model_orig(DEFAULT_MODEL_UNFILTERED)
def convert_filtered_model(): convert_model_orig(DEFAULT_MODEL_FILTERED)



def download_model_converted(model_name:str=DEFAULT_MODEL, force:bool=False):
    # @TODO
    pass

def get_model_converted(model_name:str=DEFAULT_MODEL, force:bool=False, force_convert:bool=False):
    resfn = ''
    if not force_convert: resfn = download_model_converted(model_name, force=force)
    if not resfn: resfn = convert_model_orig(model_name, force=force)
    return resfn

