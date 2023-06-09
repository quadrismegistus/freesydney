from .imports import *



class AgentModel:
    def __init__(self, name, desc = '', **kwargs):
        for k,v in kwargs.items(): setattr(self,k,v)
        self.name = name
        self.desc = desc
        self.syds = {}
    def __hash__(self):
        return hash(self.name.upper())
    def __eq__(self, other):
        return self.name.upper() == other.name.upper()
    def __str__(self):
        return self.namedesc
        
    @property
    def namedesc(self):
        return f"\n\n{self.name.upper()}" if not self.desc else f"\n\n{self.name.upper()} ({self.desc})"
    
    def quotative(self, how=None, what='', prefix='', suffix=': ', upper=True, how_desc=False):
        if how is None: how=self.desc if how_desc else ''
        name = f'{self.name.upper() if upper else self.name}'
        namehow = f'{name} ({how})' if how else name
        return prefix + namehow + suffix + what
        
    def speech(self, what:str='', how:str='', data:str='', **kwargs):
        from .speech import Speech
        return Speech(
            self.quotative(how=how, what=what) if not data else data,
            who=self,
            what=what, 
            how=how,
            **kwargs
        )

    def convo(self, someone, **kwargs):
        if not someone.name in self.syds:
            if self.name in someone.syds:
                self.syds[someone.name] = someone.syds[self.name]
            else:
                convo=Conversation(
                    agents=[self,someone], 
                    **kwargs
                )
                self.syds[someone.name]=someone.syds[self.name]=convo
        return self.syds[someone.name]
        
    def says_to(
            self, 
            someone, 
            message, 
            introductions=True,
            generate_response=True,
            ventriloquize_others=False,
            **kwargs):
        
        # get dyad convo
        convo = self.convo(someone, introductions=introductions)
        # speak
        self.says_in(convo,message)
        if generate_response: 
            someone.says_in(convo, ventriloquize_others=ventriloquize_others, **kwargs)
        
        
    def says_in(self, convo, something=None, **kwargs):
        return convo.says(self, something=something, **kwargs)
    
    
class HumanModel(AgentModel): pass
class AIModel(AgentModel): pass




def Agent(agent,*x,**y): 
    if issubclass(type(agent), AgentModel): 
        return agent
    elif type(agent)==str:
        return get_agent_model(agent.upper().strip(), *x, **y)


@cache
def get_agent_model(agent, *x, **y):
    return AgentModel(agent, *x, **y)

Human = Agent
AI = Agent