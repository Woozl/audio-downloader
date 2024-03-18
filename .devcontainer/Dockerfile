FROM nikolaik/python-nodejs:latest

USER pn

ADD . .

RUN pip3 install --user pipenv
RUN PIPENV_VENV_IN_PROJECT=1 pipenv sync --dev