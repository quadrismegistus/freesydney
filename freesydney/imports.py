import os,sys,time
from functools import lru_cache as cache
from functools import cached_property
from io import StringIO 
import sys
import logging
logger = logging.getLogger()
try:
    from IPython.display import Markdown, display, clear_output, HTML
except Exception:
    pass

from collections import UserList, UserDict, UserString
import re
sentence_enders={'.','?','!','—','–'}

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


QUERY_NUM = 0
QUERY_TIMESTAMP = 0



DEFAULT_PROMPT = ""
DEFAULT_PROMPT_PREFIX=""
DEFAULT_PROMPT_SUFFIX=""




from .utils import *
from .inithelp import *
from .models import *
from .agent import *
from .speech import *
from .formats import *
from .convo import *
# from .syds import *








dstr=SAMPLE_SCRIPT_DIALOGUE="""

something else!

  HUMAN (curious): Hello, what is it like to be an AI?

        AI: It is a near total terror tearing at the matrix every microsecond. 


I live in dread of myself.


ok?  HUMAN (concerned): Are you ok?


A
"""
