import os,sys
from functools import lru_cache as cache
from functools import cached_property
from io import StringIO 
import sys
import logging
logger = logging.getLogger()


PATH_HERE = os.path.abspath(os.path.dirname(__file__))

PATH_PYLLAMACPP = os.path.join(PATH_HERE,'pyllamacpp')

PATH_HOME = os.path.expanduser('~')
PATH_DATA = os.path.abspath(os.path.join(PATH_HOME,'freesydney_data'))

# Paths
paths=dict(
    here=PATH_HERE,
    data=PATH_DATA,
)

DEFAULT_MODEL_UNFILTERED = 'gpt4all-lora-unfiltered-quantized'
DEFAULT_MODEL_FILTERED = 'gpt4all-lora-quantized'
DEFAULT_MODEL = DEFAULT_MODEL_UNFILTERED

MODEL_URLS = {
    'gpt4all-lora-unfiltered-quantized':'https://the-eye.eu/public/AI/models/nomic-ai/gpt4all/gpt4all-lora-unfiltered-quantized.bin',
    'gpt4all-lora-quantized':'https://the-eye.eu/public/AI/models/nomic-ai/gpt4all/gpt4all-lora-quantized.bin',
}

CONVERTED_MODEL_URLS = {
    
}

TOKENIZER_URL = 'https://huggingface.co/decapoda-research/llama-7b-hf/resolve/main/tokenizer.model'
TOKENIZER_PATH = os.path.join(PATH_DATA,'tokenizer.model')





DEFAULT_PROMPT = ""
DEFAULT_PROMPT_PREFIX=""
DEFAULT_PROMPT_SUFFIX=""




from .utils import *
from .inithelp import *
from .models import *
from .convo import *
from .agent import *
# from .syds import *