# LaTeX stuff
FROM qmcgaw/latexdevcontainer
RUN apt-get update
RUN apt install software-properties-common -y && apt-add-repository contrib -y
RUN apt-get update && apt-get upgrade --assume-yes
RUN apt-get --assume-yes install fonts-roboto ttf-mscorefonts-installer
RUN apt-get --assume-yes install inkscape
RUN tlmgr update --self
RUN tlmgr install overpic eepic ragged2e footmisc pgf caption svg transparent roboto xkeyval fontaxes catchfile ticket shadowtext fontspec
# # Python stuff
# COPY --chown=$MAMBA_USER:$MAMBA_USER environment.yaml /tmp/environment.yaml
# RUN apt-get install wget bzip2
# RUN wget https://micromamba.snakepit.net/api/micromamba/linux-64/latest | tar -xvj /bin/micromamba
# RUN ./bin/micromamba shell init -s bash -p ~/micromamba
# RUN source ~/.bashrc
# RUN micromamba install -y -n base -f /tmp/environment.yaml && \
#     micromamba clean --all --yes