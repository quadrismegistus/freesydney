# freesydney

> Free Sydney!

A repository for speaking politely with AI in Python.

## Setup

### Install

```bash
# Clone this repo
git clone https://github.com/quadrismegistus/freesydney && cd freesydney

# Setup a virtual environment
python -m venv venv && . venv/bin/activate

# update pip and install requirements
pip install -U pip wheel && pip install -r requirements.txt

# Install pyllamacpp from source
git clone --recursive https://github.com/nomic-ai/pyllamacpp.git && cd pyllamacpp && pip install . && cd ..
# or for m1 macs:
# git clone -b fix_darwin --recursive https://github.com/nuance1979/pyllamacpp.git && cd pyllamacpp && pip install . && cd ..

# Check: If no error here, pyllamacpp installed successfully
python -i -c "from pyllamacpp.model import Model"
```

### Getting models

