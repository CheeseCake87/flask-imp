FROM python:3.11-alpine
WORKDIR /flask-imp
COPY app app
COPY flask_imp flask_imp
COPY .env .env
COPY pyproject.toml pyproject.toml
COPY requirements/development.txt development.txt
COPY requirements/main.txt main.txt
RUN pip install -r development.txt
RUN flit install --symlink
ENTRYPOINT ["flask", "run", "--debug", "--host=0.0.0.0"]