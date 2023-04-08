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
                newline=f'({agent.name.upper()} is {agent.desc}.)'
                self.lines.append(newline)
                self.lines_full.append(newline)
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
            verbose_prompt=True,
            verbose_response=True,
            how='',
            **kwargs):
        # get quotative
        quot = self.quotative(someone, how=how)

        # if we don't know what this person is saying, generate it
        if not something:
            # if verbose_prompt:
                # printm_blockquote(str(self), 'Prompt')

            # we're predicting what someone says
            primer = self.sep + quot
            new_lines = self.generate(
                primer=primer,
                verbose_prompt=verbose_prompt,
                verbose_response=False
            )
            new_new_lines = self.find_first_response(someone, new_lines)
            not_new_new_lines = new_lines[len(new_new_lines):]
            
            if verbose_response:
                # omd=f"""{self.sep.join(self.lines)}{self.sep}<b>{self.sep.join(new_new_lines)}</b>{self.sep}<i>{self.sep.join(not_new_new_lines)}</i>"""
                newnew=self.sep.join(new_new_lines)
                kindanew=self.sep.join(not_new_new_lines)
                omd=f"{quot}<b>{newnew}</b>{self.sep}<i>{kindanew}</i>"
                printm_blockquote(omd,'Response')

            new_lines[0] = quot + new_lines[0]
            new_new_lines[0] = quot + new_new_lines[0]
            self.lines_full.extend(new_lines)
            self.lines.extend(new_new_lines)
            
            

        else:
            newline = f'{quot}{something}'
            self.lines.append(newline)
            self.lines_full.append(newline)
        
        # record utterance
        self.uttered.add(someone)

        
    def find_first_response(self, someone, lines):
        new_new_lines = []
        others = {ag for ag in self.agents if ag is not someone}
        for line in lines:
            if any(
                line.startswith(self.quotative(ag, introduce=False))
                for ag in others
            ):
                break
            new_new_lines.append(line)
        return new_new_lines


    def generate(
            self, 
            n_predict=55, 
            primer='', 
            verbose_prompt=True,
            verbose_response=True,
            **kwargs):
        
        prompt = str(self) + primer

        response = generate(
            prompt, 
            n_predict=n_predict, 
            verbose_prompt=verbose_prompt,
            verbose_response=verbose_response, 
            **kwargs
        )
        new_lines = [x for x in response.split(self.sep) if x]
        return new_lines


        

def Convo(*x,**y):
    return Conversation(*x,**y)



