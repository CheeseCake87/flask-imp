![](https://raw.githubusercontent.com/CheeseCake87/Flask-Imp/master/_assets/Flask-Imp-Small.png)

# Flask-Imp

![Tests](https://github.com/CheeseCake87/Flask-Imp/actions/workflows/tests.yml/badge.svg)

## What is Flask-Imp?

Flask-Imp's main purpose is to help simplify the importing of blueprints, resources, and models.
It has a few extra features built in to help with securing pages and password authentication.

## Documentation

[https://cheesecake87.github.io/Flask-Imp/](https://cheesecake87.github.io/Flask-Imp/)

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
git clone https://github.com/CheeseCake87/Flask-Imp.git
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
pip install -e .
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

The test Flask app is located in the `test_app` folder. 

The tests are located in the `tests` folder.

The tests are linked to the tests blueprint located at `test_app/blueprints/tests`.
