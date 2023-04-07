from .imports import *


def get_model(model_name:str=DEFAULT_MODEL, **kwargs):
    model_fn = get_model_converted(model_name)
    ######
    ## @HACK @FIX @TODO:
    # force disable stderr output    
    def donothing(*x,**y): pass
    sys.stderr.write = donothing
    ###########
    from pyllamacpp.model import Model
    model = Model(model_fn, **kwargs)
    return model

def Model(): return BaseModel()

def Syd(*args, **kwargs): return BaseModel(*args, **kwargs)

class BaseModel:
    name=DEFAULT_MODEL
    system_prompt=''
    prompt_prefix='> '
    prompt_suffix='\n'
    prompt_joiner = '\n\n'

    def __init__(self, **kwargs):
        self._kwargs=kwargs
        self.history = []
        self.prompted = False
    
    @cached_property
    def pyllamacpp(self):
        return get_model(self.name, **self._kwargs)

    def get_prompt(self, prompt='', with_history=True):
        if self.system_prompt and not self.history:
            self.history.append(self.system_prompt)

        if prompt: 
            prompt = self.prompt_prefix + prompt + self.prompt_suffix
        if with_history: 
            prompt = self.prompt_joiner.join(self.history + ([prompt] if prompt else []))
        return prompt

    def generate(self, prompt, with_history=True, **kwargs):
        prompt = self.get_prompt(prompt, with_history=with_history)
        print("## SENDING PROMPT:\n"+prompt+"##########")
        
        # send prompt
        res = self.pyllamacpp.generate(prompt, **kwargs)
        # find response part

        print("### RESPONSE:"+true_res)
        true_res = res.split(prompt,1)[-1].strip()
        self.history.extend([prompt, true_res])
        self.res = self.prompt_joiner.join(self.history)
        return true_res

    def sayto(self, prompt, **kwargs):
        kwargs['with_history'] = True
        # kwargs['prefix'] = self.prompt_prefix
        # kwargs['suffix'] = self.prompt_suffix
        return self.generate(prompt, **kwargs)


class Responder(BaseModel): 
    system_prompt="""
Below is an instruction that describes a task. Write a response that appropriately completes the request.

> How many letters are there in the English alphabet?
There 26 letters in the English alphabet.

"""

