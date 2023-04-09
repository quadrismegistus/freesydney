from .imports import *

def Convo(*x,**y): return Conversation(*x,**y)


class Conversation:
    def __init__(self, *agents, sep='\n\n', system_prompt=''):
        self.agents = {}
        for agent in agents:
            if type(agent)==str:
                agent = Agent(name=agent)
            self.agents[agent.name.upper()] = agent
        self.sep = sep
        self.dialogue = UtteranceList()
        self.introduced = set()
        self.genstr = ''
        self.system_prompt = system_prompt

    def __str__(self):
        return self.prompt
    
    def _repr_html_(self, include_system=False):
        o=[]
        if include_system:
            o.append(md2.markdown(self.get_system_prompt()))
        
        selfmd = self.dialogue._repr_html_()

        anames = ", ".join(agent.name for agent in self.agents.values())
        return f'''
<div style="border:1px solid gray; padding:0 0.75em;">
<h3>Conversation with {anames}</h3>
{selfmd}
</div>
            '''

        
    def get_agent(self, agent_name_or_obj=None, **kwargs):
        if issubclass(type(agent_name_or_obj), Agent):
            return agent_name_or_obj
        
        elif type(agent_name_or_obj)==str:
            agent_name = agent_name_or_obj
            if not agent_name in self.agents: 
                self.agents[agent_name] = Agent(name=agent_name, **kwargs)
            return self.agents[agent_name]
        
        # else a random agent?
        if self.agents:
            return random.choice(self.agents.values())
        
        return None
                
    def get_system_prompt(self):
        dramatis_sep = "\n\n"
        namedescs = [
            f'* {agent.name.upper()}, {agent.desc}.' if agent.desc else f'* {agent.name.upper()}'
            for agent in self.agents.values()
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
        
        utter = self.get_agent(who).utter(what, how)
        utter._convo = self
        if save: utter.save()
        return utter
        
    def get_prompt(self,
            for_agent=None,
            follow_with_sep=False,
            **kwargs):
        lines = [self.get_system_prompt()]
        for utter in self.dialogue:
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
            gen_dial = self.parse_lines(genstr, primer=primer,prompt=prompt)
            if save: gen_dial.save()
            return gen_dial
        
        return UtteranceList()
        
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
    
    def extend_dialogue(self, other_list):
        for utt in other_list:
            if not any ((utt is x) for x in self.dialogue):
                self.dialogue.append(utt)
    
    def line_starts_with_a_name(self, line, among_agents=None):
        if among_agents is None: among_agents = self.agents
        return any(line.startswith(ag.name.upper()) for ag in among_agents)
    
    def parse_lines(self, string, verbose=True, primer='',prompt=''):
        utters = UtteranceList()
        utters._convo = self
        utters._prefix = ''
        utters._suffix = ''
        utters._parsed = string

        olines = []
        nolines = []
        for li,line in enumerate(string.split(self.sep)):
            if line.startswith('* '): line = line[2:]
            if not ':' in line:
                who = ''
                what = line
                how = ''

                # add to prev?
                if what and self.dialogue and not olines:
                    utters._prefix = what

            else:
                whohow,what = line.split(':', 1)
                if '(' in whohow:
                    who,how=whohow.split('(',1)
                    who = who.strip()
                    how = how.split(')',1)[0].strip()
                else:
                    who = whohow.strip()
                    how = ''
            
            if who and what.strip():# and what.strip()[-1] in sentence_enders:
                u = Utterance(
                    who=self.get_agent(who),
                    what=what.strip(),
                    how=how.strip()
                )
                utters.append(u)
                olines.append(line)
            else:
                nolines.append(line)

        utters._suffix = self.sep.join(nolines)
        return utters
        
    







