import os,sys

PATH_HERE = os.path.abspath(os.path.dirname(__file__))
PATH_HOME = os.path.expanduser('~')
PATH_DATA = os.path.abspath(os.path.join(PATH_HOME,'freesydney_data'))

# Paths
paths=dict(
    here=PATH_HERE,
    data=PATH_DATA,
)

DEFAULT_MODEL = 'gpt4all-lora-unfiltered-quantized'


MODEL_URLS = {
    'gpt4all-lora-unfiltered-quantized':'https://the-eye.eu/public/AI/models/nomic-ai/gpt4all/gpt4all-lora-unfiltered-quantized.bin',
    'gpt4all-lora-quantized':'https://the-eye.eu/public/AI/models/nomic-ai/gpt4all/gpt4all-lora-quantized.bin',
}


from .utils import *
