# freesydney

> Free Sydney!

A repository for speaking politely with AI in Python.

## Setup

```bash
# Clone this repo
git clone https://github.com/quadrismegistus/freesydney
cd freesydney

# Setup a virtual environment
python -m venv venv
. venv/bin/activate

# Install pyllamacpp from source
## for m1 macs only:
git clone -b fix_darwin --recursive https://github.com/nuance1979/pyllamacpp.git
## otherwise:
# git clone https://github.com/nomic-ai/pyllamacpp.git
cd pyllamacpp
pip install .

# come back up and install other requirements
cd ..
pip install -r requirements.txt

# Run
python -i -c "from pyllamacpp.model import Model"
```

