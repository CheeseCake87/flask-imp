![](https://raw.githubusercontent.com/CheeseCake87/Flask-BigApp/master/_assets/Flask-BigApp-v2.png)

# Flask-BigApp

![Tests](https://github.com/CheeseCake87/Flask-BigApp/actions/workflows/tests.yml/badge.svg)

Current Version: `2.0.0`

## What is Flask-BigApp?

Flask-BigApp's main purpose is to help simplify the importing of blueprints, resources and models.
It has a few extra features built in to help with securing pages and password authentication.

## Getting Started

### Setup

(This assumes you have Python installed)

1. Download or Clone this repository.
2. Open terminal (Linux) / powershell (Windows) and cd to the directory of the project.

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

### Install Flask-BigApp

```bash
pip install flask-bigapp
```

### Create a new project

```bash
flask-bigapp init
```

### Run the project

```bash
flask run --debug
```