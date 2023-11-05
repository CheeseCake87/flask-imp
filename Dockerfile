FROM python:3.11-alpine
WORKDIR /flask-imp
COPY app app
COPY src src
COPY .env .env
COPY pyproject.toml pyproject.toml
COPY requirements.txt requirements.txt
COPY setup.py setup.py
RUN pip install -r requirements.txt
RUN python3 setup.py install
ENTRYPOINT ["flask", "run", "--debug", "--host=0.0.0.0"]