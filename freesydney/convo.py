from .imports import *

def Convo(*x,**y): return Conversation(*x,**y)


class Conversation:
    def __init__(self, *agents, sep='\n\n', system_prompt=''):
        self.agents = set(agents)
        self.sep = sep
        self.system_prompt = system_prompt
        self.speeches = Speeches(_convo=self)
        self.introduced = set()
        self.genstr = ''

    def __str__(self):
        return self.prompt
    
    def _repr_html_(self, include_system=False):
        selfmd = self.speeches._repr_html_()
        anames = ", ".join(agent.name for agent in self.agents)
        return f'''<div style="border:1px solid gray; padding:0 0.75em;"><h3>Conversation with {anames}</h3>{selfmd}</div>'''
                
    def get_system_prompt(self):
        dramatis_sep = "\n\n"
        namedescs = [
            f'* {agent.name.upper()}, {agent.desc}.' if agent.desc else f'* {agent.name.upper()}'
            for agent in self.agents
        ]
        # if len(namedescs)>1: namedescs[-1]='and '+namedescs[-1]
        ostr=f'''Dramatis Personae:

{dramatis_sep.join(namedescs)}

----

Dialogue:

'''
        return ostr
    
    def speech(self, 
             who:'Agent', 
             what:str, 
             save=True,
             how=None):
        speech = Agent(who).speech(what, how)
        speech._convo = self
        if save: speech.save()
        return speech
        
    def get_prompt(self,
            for_agent=None,
            follow_with_sep=False,
            **kwargs):
        lines = [self.get_system_prompt()]
        for utter in self.speeches:
            lines.append(str(utter))
        if for_agent:
            follow_with_sep = False
            lines.append(self.get_agent(for_agent).quotative())
        return self.sep.join(lines) + (self.sep if follow_with_sep else '')
    
    @property
    def prompt(self): return self.get_prompt()
    
    def generate_str(self, prompt='', primer='', **kwargs):
        if not prompt: prompt = self.get_prompt(**kwargs)
        genstr=primer + generate(prompt + primer, **kwargs)
        self.genstr = genstr
        return genstr
    
    def generate_dialogue(self, prompt='', primer='', next_speaker='', save=False, **kwargs):
        if not primer and next_speaker:
            primer=self.sep+self.get_agent(next_speaker).quotative()

        # get prompt
        if not prompt: prompt = self.get_prompt(**kwargs)
        
        genstr = self.generate_str(
            prompt=prompt,
            primer=primer,
            **kwargs
        )
            
        if genstr:
            gen_dial = Speeches.parse(genstr)
            gen_dial._convo = self
            if save: gen_dial.save()
            return gen_dial
        
        return Speeches(_convo=self)
        
    def generate(self, save=False, **kwargs):
        return self.generate_dialogue(save=save, **kwargs)

    def generate_options(self, n=2, verbose = True, **kwargs):
        kwargs['save']=False
        opts = [
            self.generate(**kwargs)
            for i in range(n)
        ]
        if verbose:
            try:
                clear_output(wait=True)
                for i,opt in enumerate(opts):
                    printm(f'### Option {i+1}')
                    display(opt)
            except Exception:
                pass
        return opts
    
    def gensave(self, **kwargs):
        kwargs['save']=True
        return self.generate(**kwargs)
    
    
    