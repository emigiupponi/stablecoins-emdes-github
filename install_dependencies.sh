#!/bin/bash

# Instalar dependencias de Python
pip install boto3 python-dotenv kaleido

# Actualizar la lista de paquetes disponibles
sudo apt-get update

# Instalar chktex, latexmk y texlive-latex-base
sudo apt-get install -y chktex latexmk texlive-latex-base