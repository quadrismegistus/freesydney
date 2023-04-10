from .imports import *

class TextFormat: 
    pass

class ScriptFormat(TextFormat):

    def parse_speeches(string,sep='\n\n'):
        speeches_l = []

        for para in string.split(sep):
            speech_sents = []

            for sent in tokenize_sentences(para):
                if ':' in sent:
                    name = sent.split(':')[0].split('(')[0].split('[')[0].strip()
                    if name and name==name.upper():
                        if speech_sents:
                            speeches_l.append(ScriptFormat.parse_speech(speech_sents))
                            speech_sents = []
                speech_sents.append(sent)
        
            if speech_sents:
                speeches_l.append(ScriptFormat.parse_speech(speech_sents))
        
        return Speeches(speeches_l, sep=sep, string=string)
    
    def parse_speech(line):
        line = ''.join(line) if type(line)==list else line
        who,what,how = ScriptFormat.get_who_what_how(line)
        if who and what:# and what.strip()[-1] in sentence_enders:
            return Speech(
                line,
                who=Agent(who.strip()),
                what=what,
                how=how
            )
        return Speech(line)
        
    
    def get_who_what_how(target_string):
        # This regular expression pattern matches "SPEAKER (stage_direction): " followed by any non-digit character.
        #pattern = r'(?P<who>[A-Za-z]+)(?:\s+\((?P<how>[^)]+)\))?:\s+(?P<what>[^\d]+)'
        # pattern = r'(?P<who>[A-Za-z]+(?:\s+[A-Za-z]+)*)(?:\s+\((?P<how>[^)]+)\))?:\s+(?P<what>[^\d]+)'
        pattern = r'(?P<who>[A-Za-z]+(?:\s+[A-Za-z]+)*)(?:\s+[\[\(](?P<how>[^\]\)]+)[\]\)])?:\s+(?P<what>[^\d]+)'



        # Use the finditer method to find all matches of the pattern in the target string.
        matches = re.finditer(pattern, target_string)
        
        # Iterate over the matches and extract the speaker, stage direction, and speech text.
        # Return first
        for match in matches:
            return (match.group('who'), match.group('what'), match.group('how'))
        return ('','','')