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
            agent_name = agent_name_or_obj.upper()
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
    
    def says(self, 
             who:'Agent', 
             what:str, 
             how=None):
        
        utter = self.get_agent(who).utter(what, how)
        self.dialogue.append(utter)
        
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
    
    def generate_str(self, primer='', **kwargs):
        prompt = self.get_prompt(**kwargs)
        genstr=primer + generate(prompt + primer, verbose_response=False)
        self.genstr = genstr
        return genstr
    
    def generate_dialogue(self, primer='', next_speaker='', save=False, **kwargs):
        if not primer and next_speaker:
            primer=self.sep+self.get_agent(next_speaker).quotative()
        
        genstr = self.generate_str(
            primer=primer, 
            verbose_response=False, 
            **kwargs
        )
            
        if genstr:
            gen_dial = self.parse_lines(genstr, primer=primer)
            if save: gen_dial.save()
            return gen_dial
        
        return UtteranceList()
        
    def generate(self, save=True, **kwargs):
        return self.generate_dialogue(save=save, **kwargs)
    gen = generate
    
    def gensave(self, save=True, **kwargs):
        return self.generate(save=save, **kwargs)
    
    def extend_dialogue(self, other_list):
        for utt in other_list:
            if not any ((utt is x) for x in self.dialogue):
                self.dialogue.append(utt)
    
    def line_starts_with_a_name(self, line, among_agents=None):
        if among_agents is None: among_agents = self.agents
        return any(line.startswith(ag.name.upper()) for ag in among_agents)
    
    def parse_lines(self, string, verbose=True, primer=''):
        utters = UtteranceList()
        utters._convo = self

        olines = []
        nolines = []
        for line in string.split(self.sep):
            if line.startswith('* '): line = line[2:]
            if not ':' in line:
                who = ''
                what = line
                how = ''
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
        
        # printm_blockquote(self.sep.join(olines), 'Response')
        printm_blockquote_bi(
            primer,
            self.sep.join(olines)[len(primer):]+self.sep,
            self.sep.join(nolines)+self.sep,
            sep='',
            header='Response'
        )

        return utters
        
    









# class Conversation:
#     def __init__(self, agents=[], sep='\n\n', introductions=True, dramatis = False):
#         self.agents = set()
#         self.lines = []
#         self.lines_full = []
#         self.uttered = set()
#         self.introduced = set()
#         self.introductions = introductions
#         self.dramatis = dramatis
#         self.sep = sep
        
#         ## add agents
#         if dramatis: 
#             self.add_line_both('#### CHARACTERS')
#         for agent in agents: 
#             self.add_agent(
#                 agent, 
#                 introduce=introductions
#             )
#         if dramatis: 
#             # self.add_line_both('----------')
#             self.add_line_both('#### DIALOGUE')
    
#     def __str__(self, joiner=None):
#         if joiner is None: joiner=self.sep
#         return self.sep.join(self.lines)
    
    # def _repr_html_(self):
    #     import markdown2 as md2
    #     selfmd=md2.markdown(str(self))
    #     return f'''
    #         <div style="font-weight:bold;">Conversation with {", ".join(agent.name for agent in self.agents)}]</div>
    #         <blockquote>
    #         {selfmd}
    #         </blockquote>
    #         '''


#     def add_line_both(self, newline):
#         self.lines.append(newline)
#         self.lines_full.append(newline)

#     def add_agent(self, agent, introduce=True, bullet_point=False):
#         if not agent in self.agents:
#             self.agents.add(agent)
#             if introduce:
#                 newline=f'({agent.name.upper()}, is {agent.desc}.)'
#                 if bullet_point: newline='* '+newline
#                 self.lines.append(newline)
#                 self.lines_full.append(newline)
#                 self.introduced.add(agent)
        
#     def has_introduced(self, someone):
#         return someone in self.introduced or someone in self.uttered

#     def quotative(self, someone, how='', introduce=True, upper=True, bullet_point=False):
#         name = f'{someone.name.upper() if upper else someone.name}'
#         if how:
#             direction = how
#         elif introduce and not self.has_introduced(someone):
#             direction = someone.desc
#         else:
#             direction = ''
        
#         o = f'{name} ({direction}): ' if direction else f'{name}: '
#         if bullet_point: o='* '+o
#         return o
        
#     def says(
#             self, 
#             someone, 
#             something=None, 
#             verbose_prompt=True,
#             verbose_response=True,
#             how='',
#             **kwargs):
#         # get quotative
#         quot = self.quotative(someone, how=how)

#         # if we don't know what this person is saying, generate it
#         if not something:
#             # if verbose_prompt:
#                 # printm_blockquote(str(self), 'Prompt')

#             # we're predicting what someone says
#             primer = self.sep + quot
#             new_lines = self.generate(
#                 primer=primer,
#                 verbose_prompt=verbose_prompt,
#                 verbose_response=False
#             )
#             new_new_lines = self.find_first_response(someone, new_lines)
#             not_new_new_lines = new_lines[len(new_new_lines):]
            
#             if verbose_response:
#                 printm_blockquote_bi(
#                     '',
#                     self.sep.join(new_new_lines),
#                     self.sep.join(not_new_new_lines),
#                     sep=self.sep,
#                     header='Response'
#                 )
#             # new_lines[0] = quot + new_lines[0]
#             # new_new_lines[0] = quot + new_new_lines[0]
#             self.lines_full.extend(new_lines)
#             self.lines.extend(new_new_lines)
            
            

#         else:
#             newline = f'{quot}{something}'
#             self.lines.append(newline)
#             self.lines_full.append(newline)
        
#         # record utterance
#         self.uttered.add(someone)

#     def extend(
#             self, 
#             on_new_line=True, 
#             primer='', 
#             is_safe_func=None,
#             return_lines=False,
#             verbose_response=True,
#             **kwargs):

#         prompt = str(self) + primer


#     def carry_on(
#             self, 
#             on_new_line=True, 
#             primer='', 
#             return_lines=False,
#             verbose_response=True,
#             **kwargs):
        
#         if on_new_line: primer=self.sep+primer
        
#         # extend full lines
#         new_lines = self.generate(
#             primer=primer, 
#             verbose_response=False,
#             **kwargs
#         )

#         # safe lines?
#         safe_lines = (
#             new_lines[:-1] 
#             if (
#                 len(new_lines)>1 
#                 and not 
#                 self.line_starts_with_a_name(new_lines[-1])
#              ) else new_lines
#         )
#         notsafe_lines = new_lines[len(safe_lines):]

#         # save
#         if verbose_response:
#             printm_blockquote_bi(
#                 '', #self.sep.join(self.lines),
#                 self.sep.join(safe_lines),
#                 self.sep.join(notsafe_lines),
#                 sep=self.sep,
#                 header='Response'
#             )



#         extend_sticky(self.lines_full, new_lines)
#         extend_sticky(self.lines, safe_lines)
#         if return_lines: return safe_lines

#     def line_starts_with_a_name(self, line, among_agents=None):
#         if among_agents is None: among_agents = self.agents
#         return any(
#             line.startswith(
#                 # self.quotative(ag, introduce=False, how='')
#                 ag.name.upper()
#             )
#             for ag in among_agents
#         )

        
#     def find_first_response(self, someone, lines):
#         new_new_lines = []
#         others = {ag for ag in self.agents if ag is not someone}
#         for line in lines:
#             if any(
#                 # line.startswith(self.quotative(ag, introduce=False))
#                 line.startswith(ag.name.upper())
#                 for ag in others
#             ):
#                 break
#             new_new_lines.append(line)
#         return new_new_lines


#     def generate(
#             self, 
#             prompt = '',
#             n_predict=55, 
#             primer='', 
#             verbose_prompt=True,
#             verbose_response=True,
#             **kwargs):
        
#         prompt = (str(self) if not prompt else prompt) + primer

#         response = generate(
#             prompt, 
#             n_predict=n_predict, 
#             verbose_prompt=verbose_prompt,
#             verbose_response=verbose_response, 
#             **kwargs
#         )
#         # new_lines = [x for x in response.split(self.sep) if x]
#         # new_lines = (primer+response).split(self.sep)
#         new_lines = response.split(self.sep)
#         return new_lines


        
