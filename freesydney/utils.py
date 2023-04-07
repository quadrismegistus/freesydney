from .imports import *


def get_tqdm(*args,progress=True,**kwargs):
    if not progress: return get_first(args)
    if 0: #in_jupyter():
        from tqdm.notebook import tqdm as tqdmx
    else:
        from tqdm import tqdm as tqdmx
    return tqdmx(*args,**kwargs)

def in_jupyter(): return sys.argv[-1].endswith('json')



def ensure_dir(dirname):
    if not os.path.exists(dirname):
        try:
            os.makedirs(dirname)
        except OSError as e:
            pass
            #print(e)
            #log.error(e)



#!/usr/bin/env python 
__author__  = "github.com/ruxi"
__license__ = "MIT"
def download(url, filename=False, verbose = False, desc=None):
    """
    Download file with progressbar
    """


    import requests 
    from tqdm import tqdm
    import os.path


    if not filename:
        local_filename = os.path.join(".",url.split('/')[-1])
    else:
        local_filename = filename

    ensure_dir(os.path.dirname(local_filename))
    
    r = requests.get(url, stream=True)
    file_size = r.headers.get('content-length')
    chunk = 1
    chunk_size=1024
    num_bars = int(file_size) // chunk_size if file_size else None
    if verbose>0:
        print(dict(file_size=file_size))
        print(dict(num_bars=num_bars))

    
    with open(local_filename, 'wb') as fp:
        iterr=get_tqdm(
            r.iter_content(chunk_size=chunk_size),
            total=num_bars,
            unit='KB',
            desc = local_filename if not desc else desc,
            leave = True
        )
        for chunk in iterr:
            fp.write(chunk)
    return




class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self
    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio    # free up some memory
        sys.stdout = self._stdout


def printm(*x,joiner=' ',**y):
    try:
        from IPython.display import Markdown, display
        display(Markdown(joiner.join(str(xx) for xx in x)))
    except Exception:
        print(*x,**y)

def printm_blockquote(content, header):
    o=f"#### {header}\n" if header else ""
    o+=f"<blockquote>\n{content}\n</blockqute>"
    printm(o)