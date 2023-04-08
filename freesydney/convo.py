from .imports import *

class Conversation:
    def __init__(self, agents=[], sep='\n\n', introductions=True):
        self.agents = set()
        self.lines = []
        self.lines_full = []
        self.uttered = set()
        self.introduced = set()
        self.introductions = introductions
        self.sep = sep
        
        ## add agents
        for agent in agents: 
            self.add_agent(agent, introduce=self.introductions)
    
    def __str__(self, joiner='\n\n'):
        return joiner.join(self.lines)

    def add_agent(self, agent, introduce=True):
        if not agent in self.agents:
            self.agents.add(agent)
            if introduce:
                self.lines.append(f'({agent.name.upper()} is {agent.desc}.)')
                self.introduced.add(agent)
        
    def has_introduced(self, someone):
        return someone in self.introduced or someone in self.uttered

    def quotative(self, someone, how='', introduce=True, upper=True):
        name = f'{someone.name.upper() if upper else someone.name}'
        if how:
            direction = how
        elif introduce and not self.has_introduced(someone):
            direction = someone.desc
        else:
            direction = ''
        
        o = f'{name} ({direction}): ' if direction else f'{name}: '
        return o
        
    def says(
            self, 
            someone, 
            something=None, 
            how='',
            ventriloquize_others=True,
            generate=True, 
            someone_replies=None,
            **kwargs):
        
        quot = self.quotative(someone, how=how)
        if not something:
            # we're predicting what someone says
            new_new_lines = new_lines = self.generate(primer=self.sep + quot)
            print('new_lines',new_lines)
            if not ventriloquize_others:
                new_new_lines = []
                others = {ag for ag in self.agents if ag != someone}
                for line in new_lines:
                    if any(
                        line.startswith(self.quotative(ag, introduce=False))
                        for ag in others
                    ):
                        break
                    new_new_lines.append(line)
                    print('new_new_lines',new_new_lines)
        else:
            new_new_lines = new_lines = [f'{quot}{something}']
        self.lines_full.extend(new_lines)
        self.lines.extend(new_new_lines)
        self.uttered.add(someone)

        



    def generate(self, n_predict=55, primer='', **kwargs):
        old = str(self)
        prompt = old + primer
        response = generate(prompt, n_predict=n_predict, **kwargs)
        print(f'RESPONSE:::\n{response}')
        new_in_response = response.split(old,1)[-1]
        # return new_in_response
        new_lines = new_in_response.split(self.sep)
        return new_lines
        # self.lines.extend([x for x in new_lines if x.strip()])


        

def Convo(*x,**y):
    return Conversation(*x,**y)



