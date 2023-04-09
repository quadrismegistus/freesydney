from .imports import *

class Agent:
    def __init__(self, name, desc = '', **kwargs):
        for k,v in kwargs.items(): setattr(self,k,v)
        self.name = name
        self.desc = desc
        self.syds = {}
    def __hash__(self):
        return hash((self.name, self.desc))
    def __eq__(self, other):
        return (self.name, self.desc) == (other.name, other.desc)
    
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
        
    def utter(self, what:str='', how:str='', **kwargs):
        return Utterance(
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
    
    
class Human(Agent):
    pass

class AI(Agent):
    pass