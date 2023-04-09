from .imports import *


class Utterance:
    def __init__(self, who:'Agent', what:str, how=''):
        self.who=who
        self.what=what
        self.how=how
    
    def __str__(self):
        return self.who.quotative(
            how=self.how, 
            what=self.what
        )

    def __repr__(self): return str(self)

    def _repr_html_(self):
        how=f' (<i>{self.how}</i>)' if self.how else ''
        o = f'<li class="speech"><b>{self.who.name}</b>{how}: {self.what}</li>'
        return o

class UtteranceList(UserList):
    def save(self):
        if hasattr(self,'_convo') and self._convo is not None:
            self._convo.extend_dialogue(self)

    def _repr_html_(self):
        selfmd = '\n\n'.join(utt._repr_html_() for utt in self)
        anames = ", ".join(utt.who.name for utt in self)
        return f'''
<div style="border:1px solid gray; padding:0 0.75em; margin:0; margin-bottom:1em;">
<h4>Utterances from {anames}</h4>
<ol style="margin:0; padding:0; margin-left: 1em; margin-bottom:1em;">
{selfmd}
</ol>
</div>
'''