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
        verbose_prompt=True,
        verbose_response=True,
        model_name=DEFAULT_MODEL,
        model_opts={},
        n_predict=66,
        keep_prompt=False,
        **generate_opts
    ):

    if verbose_prompt: printm_blockquote(prompt, 'Prompt')

    model = get_model(model_name, **model_opts)
    
    def gen(prompt):
        return model.generate(
            prompt,
            n_predict=n_predict,
            **generate_opts
        )
    
    try:
        res = gen(prompt)
    except UnicodeDecodeError as e:
        try:
            from unidecode import unidecode
            res = gen(unidecode(prompt))
        except Exception as e:
            logger.error(e)
            # get res -- however far it got
            res = model.res
        
    # find response part
    true_res = res.split(prompt,1)[-1]
    
    if verbose_response:
        # printm_blockquote(f'{prompt}<b>{true_res}</b>', 'Response')
        # printm_blockquote(f'<b>{true_res}</b>', 'Response')
        printm_blockquote(true_res, 'Response')
    
    return true_res if not keep_prompt else res
