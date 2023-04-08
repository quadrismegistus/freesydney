from .imports import *


@cache
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


def generate(
        prompt, 
        prefix="",
        suffix="", 
        **kwargs):
    return BaseModel(
        prompt_prefix=prefix,
        prompt_suffix=suffix,
    ).generate(
        prompt
    )

def Model(): return BaseModel()

def Syd(*args, **kwargs): return BaseModel(*args, **kwargs)

class BaseModel:
    def __init__(
            self,
            model_name=DEFAULT_MODEL,
            system_prompt=DEFAULT_PROMPT,
            prompt_prefix=DEFAULT_PROMPT_PREFIX,
            prompt_suffix=DEFAULT_PROMPT_SUFFIX,
            model_kwargs = {},
            **kwargs):
        
        self.model_name = model_name
        self.system_prompt = system_prompt
        self.prompt_prefix = prompt_prefix
        self.prompt_suffix = prompt_suffix
        self.model_kwargs=model_kwargs
        self.history = str(system_prompt)
        self.full_history = str(system_prompt)
        self.prompted = False
    
    @cached_property
    def pyllamacpp(self):
        return get_model(self.model_name, **self.model_kwargs)


    def generate(
            self, 
            prompt, 
            with_history=True,
            with_full_history=False,
            n_predict=55,
            prefix=None,
            suffix=None, 
            **kwargs):
        prompt_presuf = (self.prompt_prefix if prefix is None else prefix) + prompt + (self.prompt_suffix if suffix is None else suffix)
        if with_full_history:
            prompt_full = self.full_history + prompt_presuf
        elif with_history:
            prompt_full = self.history + prompt_presuf
        else:
            prompt_full = self.system_prompt + prompt_presuf
        
        printm_blockquote(prompt_full, 'Prompt')
        
        # send prompt
        try:
            res = self.pyllamacpp.generate(
                prompt_full, 
                n_predict=n_predict, 
                **kwargs
            )
        except UnicodeDecodeError as e:
            try:
                from unidecode import unidecode
                res = self.pyllamacpp.generate(
                    unidecode(prompt_full), 
                    n_predict=n_predict, 
                    **kwargs
                )
            except Exception as e:
                logger.error(e)
                # get res -- however far it got
                res = self.pyllamacpp.res
        
        

        # find response part
        true_res = res.split(prompt_full,1)[-1]
        #if true_res!=res: true_res = self.prompt_suffix + true_res
        # Did it go tooo far?
        true_true_res = true_res.split(self.prompt_prefix,1)[0] if self.prompt_prefix else true_res
        if true_true_res!=true_res:
            true_true_res_after = self.prompt_prefix + true_res.split(self.prompt_prefix,1)[-1]
            omd = f'{prompt_full} <b>{true_true_res}</b> {true_true_res_after}'
        else:
            omd = f'{prompt_full} <b>{true_res}</b>'
        
        printm_blockquote(omd, 'Response')

        self.history = prompt_full + true_true_res
        self.full_history = prompt_full + true_res

        return true_true_res

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

