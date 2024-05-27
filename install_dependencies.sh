#!/bin/bash

# Instalar dependencias de Python
pip install boto3 python-dotenv kaleido

# Instalar chktex y latexmk
sudo apt-get update
sudo apt-get install -y chktex latexmk