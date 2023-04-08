from .imports import *

class Conversation:
    def __init__(self, agents=[], sep='\n\n', introductions=True, dramatis = False):
        self.agents = set()
        self.lines = []
        self.lines_full = []
        self.uttered = set()
        self.introduced = set()
        self.introductions = introductions
        self.dramatis = dramatis
        self.sep = sep
        
        ## add agents
        if dramatis: 
            self.add_line_both('#### CHARACTERS')
        for agent in agents: 
            self.add_agent(
                agent, 
                introduce=introductions
            )
        if dramatis: 
            # self.add_line_both('----------')
            self.add_line_both('#### DIALOGUE')
    
    def __str__(self, joiner=None):
        if joiner is None: joiner=self.sep
        return self.sep.join(self.lines)
    
    def _repr_html_(self):
        import markdown2 as md2
        selfmd=md2.markdown(str(self))
        return f'''
            <div style="font-weight:bold;">Conversation with {", ".join(agent.name for agent in self.agents)}]</div>
            <blockquote>
            {selfmd}
            </blockquote>
            '''


    def add_line_both(self, newline):
        self.lines.append(newline)
        self.lines_full.append(newline)

    def add_agent(self, agent, introduce=True, bullet_point=False):
        if not agent in self.agents:
            self.agents.add(agent)
            if introduce:
                newline=f'({agent.name.upper()}, is {agent.desc}.)'
                if bullet_point: newline='* '+newline
                self.lines.append(newline)
                self.lines_full.append(newline)
                self.introduced.add(agent)
        
    def has_introduced(self, someone):
        return someone in self.introduced or someone in self.uttered

    def quotative(self, someone, how='', introduce=True, upper=True, bullet_point=False):
        name = f'{someone.name.upper() if upper else someone.name}'
        if how:
            direction = how
        elif introduce and not self.has_introduced(someone):
            direction = someone.desc
        else:
            direction = ''
        
        o = f'{name} ({direction}): ' if direction else f'{name}: '
        if bullet_point: o='* '+o
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
                printm_blockquote_bi(
                    '',
                    self.sep.join(new_new_lines),
                    self.sep.join(not_new_new_lines),
                    sep=self.sep,
                    header='Response'
                )
            # new_lines[0] = quot + new_lines[0]
            # new_new_lines[0] = quot + new_new_lines[0]
            self.lines_full.extend(new_lines)
            self.lines.extend(new_new_lines)
            
            

        else:
            newline = f'{quot}{something}'
            self.lines.append(newline)
            self.lines_full.append(newline)
        
        # record utterance
        self.uttered.add(someone)

    def extend(
            self, 
            on_new_line=True, 
            primer='', 
            is_safe_func=None,
            return_lines=False,
            verbose_response=True,
            **kwargs):

        prompt = str(self) + primer


    def carry_on(
            self, 
            on_new_line=True, 
            primer='', 
            return_lines=False,
            verbose_response=True,
            **kwargs):
        
        if on_new_line: primer=self.sep+primer
        
        # extend full lines
        new_lines = self.generate(
            primer=primer, 
            verbose_response=False,
            **kwargs
        )

        # safe lines?
        safe_lines = (
            new_lines[:-1] 
            if (
                len(new_lines)>1 
                and not 
                self.line_starts_with_a_name(new_lines[-1])
             ) else new_lines
        )
        notsafe_lines = new_lines[len(safe_lines):]

        # save
        if verbose_response:
            printm_blockquote_bi(
                '', #self.sep.join(self.lines),
                self.sep.join(safe_lines),
                self.sep.join(notsafe_lines),
                sep=self.sep,
                header='Response'
            )



        extend_sticky(self.lines_full, new_lines)
        extend_sticky(self.lines, safe_lines)
        if return_lines: return safe_lines

    def line_starts_with_a_name(self, line, among_agents=None):
        if among_agents is None: among_agents = self.agents
        return any(
            line.startswith(
                # self.quotative(ag, introduce=False, how='')
                ag.name.upper()
            )
            for ag in among_agents
        )

        
    def find_first_response(self, someone, lines):
        new_new_lines = []
        others = {ag for ag in self.agents if ag is not someone}
        for line in lines:
            if any(
                # line.startswith(self.quotative(ag, introduce=False))
                line.startswith(ag.name.upper())
                for ag in others
            ):
                break
            new_new_lines.append(line)
        return new_new_lines


    def generate(
            self, 
            prompt = '',
            n_predict=55, 
            primer='', 
            verbose_prompt=True,
            verbose_response=True,
            **kwargs):
        
        prompt = (str(self) if not prompt else prompt) + primer

        response = generate(
            prompt, 
            n_predict=n_predict, 
            verbose_prompt=verbose_prompt,
            verbose_response=verbose_response, 
            **kwargs
        )
        # new_lines = [x for x in response.split(self.sep) if x]
        # new_lines = (primer+response).split(self.sep)
        new_lines = response.split(self.sep)
        return new_lines


        

def Convo(*x,**y):
    return Conversation(*x,**y)



def printm_blockquote_bi(pre='', bold='', ital='', sep='', header=''):
    omd=f"{pre}{sep}<b>{bold}</b>{sep}<i>{ital}</i>{sep}"
    printm_blockquote(omd,header)