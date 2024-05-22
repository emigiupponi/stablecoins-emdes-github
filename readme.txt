# En Codespace hay que instalar dependencias de latex:

sudo apt-get update
sudo apt-get install texlive-latex-base

# Y luego:

sudo apt-get install latexmk

# Y para compilar, para que se compile en una subcarpeta, hay que hacerlo desde la línea de comando. 

latexmk -pdf -output-directory=pdf-compilation nombre_de_tu_documento.tex




