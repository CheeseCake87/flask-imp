![](https://raw.githubusercontent.com/CheeseCake87/Flask-Imp/master/_assets/Flask-Imp-Small.png)

# Flask-Imp

![tests](https://github.com/CheeseCake87/flask-imp/actions/workflows/tests.yml/badge.svg)
[![PyPI version](https://img.shields.io/pypi/v/flask-imp)](https://pypi.org/project/flask-imp/)
[![License](https://img.shields.io/badge/license-LGPL_v2-red.svg)](https://raw.githubusercontent.com/CheeseCake87/flask-imp/master/LICENSE)
![Downloads](https://static.pepy.tech/badge/flask-imp)
![black](https://img.shields.io/badge/code%20style-black-000000.svg)

## What is Flask-Imp?

Flask-Imp's main purpose is to help simplify the importing of blueprints, resources, and models.
It has a few extra features built in to help with securing pages and password authentication.

## Documentation

[https://cheesecake87.github.io/flask-imp/](https://cheesecake87.github.io/flask-imp/)

## Getting Started

### Setup.

Create a new project folder and navigate to it.

```text
# Linux
cd /path/to/project-folder

# Windows
cd C:\path\to\project-folder
```

### Create a virtual environment and activate it.

**Linux / MacOS**

```bash
python3 -m venv venv
```

```bash
source venv/bin/activate
```

**Windows**

```bash
python -m venv venv
```

```bash
.\venv\Scripts\activate
```

### Install Flask-Imp

```bash
pip install flask-imp
```

### Create a new project.

```bash
flask-imp init
```

---

## Working on this project.

### Setup.

**Create a new project folder and navigate to it in the terminal, then clone this repository.**

```bash
git clone https://github.com/CheeseCake87/flask-imp.git
```

### Create a virtual environment and activate it.

**Linux / MacOS**

```bash
python3 -m venv venv
```

```bash
source venv/bin/activate
```

**Windows**

```bash
python -m venv venv
```

```bash
.\venv\Scripts\activate
```

### Install the requirements.

```bash
pip install -r requirements.txt
pip install -r requirements_dev.txt
```

### Install the local version of Flask-Imp.

```bash
flit install
```

### Run the included Flask app.

```bash
Flask run --debug
```

### Run the tests.

```bash
pytest
```

### Run the tests under multiple Python versions using docker.

```bash
python3 test_docker
```

### Info

The Flask app is located in the `app` folder.

The tests are located in the `tests` folder.

The test Flask app is located in the `tests/test_app` folder. 

The tests are linked to the tests blueprint located at `test_app/blueprints/tests`.

### Building the docs.

All docs are generated from the [docs_md](docs_md) folder. Edit these files then run the following command to generate the docs.

```bash
flask --app gdocs compile
```

You can set it to watch for changes and automatically recompile the docs by adding the `--watch` flag.

```bash
flask --app gdocs compile --watch
```
