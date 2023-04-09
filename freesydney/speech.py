from .imports import *

class Speech(UserString):
    def __init__(self, data:str, who='', what='', how='', _convo=None):
        super().__init__(data)
        self.who=who
        self.what=what
        self.how=how
        self._convo=_convo
    
    def __str__(self): return self.data
    def __repr__(self): return str(self).replace('\n', ' ').strip()
    @property
    def is_valid(self): return bool(self.who and self.what)

    def _repr_html_(self):
        if not self.is_valid:
            return f'<p class="nonspeech" style="opacity:0.5">{self.data}</p>'
        else:
            how=f' (<i>{self.how}</i>)' if self.how else ''
            return  f'<p class="speech" style="margin-bottom:1em;"><b>{self.who.name.upper()}{how}</b>: {self.what}</p>'

    def save(self):
        if self._convo is not None: 
            self._convo.speeches.add_speech(self)
    
    def parse(string):
        from .formats import ScriptFormat
        res = ScriptFormat.parse_speech(string)
        if res is not None: return res

    def __add__(self, other):
        return Speech(
            data=self.data + other.data,
            who=self.who or other.who,
            what=self.what + (other.what if other.what else other.data) if self.what else '',
            how=self.how + other.how if self.how and other.how else self.how,
        )



class Speeches(UserList):
    def __init__(
        self, 
        data=[],
        string='',
        sep='\n\n',
        _convo=None
        ):

        # init as list
        super().__init__(data)
        self.string=string
        self.sep=sep
        self._convo = _convo

    def has_speech(self, speech):
        return any((speech is x) for x in self)

    def add_speech(self, speech, force=False):
        if force or not self.has_speech(speech):
            self.data.append(speech)
            self.string+=speech.data
        
    def extend(self,speeches):
        for speech in speeches:
            self.add_speech(speech)

    def _repr_html_(self):
        selfmd = '\n\n'.join(utt._repr_html_() for utt in self)
        anames = ", ".join(utt.who.name for utt in self if utt and utt.who)
        return f'''<div style="border:1px solid gray; padding:0 0.75em; margin:0; margin-bottom:1em;"><h4>Speeches from {anames}</h4><ol style="margin:0; padding:0; margin-left: 1em; margin-bottom:1em;">{selfmd}</ol></div>'''    

    @property
    def string_content(self): return self.string[len(self.string_prefix):(-len(self.string_suffix) if self.string_suffix else None)]

    @property
    def is_valid(self):
        return self.who and self.what

    def save(self):
        if self._convo is not None:
            self._convo.speeches.extend(self)

    def parse(string):
        from .formats import ScriptFormat
        res = ScriptFormat.parse_speeches(string)
        if res is not None: return res
