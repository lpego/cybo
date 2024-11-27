FROM qmcgaw/latexdevcontainer
RUN apt-get update
RUN apt --assume-yes install fonts-roboto
RUN apt-get --assume-yes install inkscape
RUN tlmgr update --self
RUN tlmgr install overpic eepic ragged2e footmisc pgf caption svg transparent roboto xkeyval fontaxes catchfile