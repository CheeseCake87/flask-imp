## Contributing to Flask-Imp

Thank you for considering contributing to Flask-Imp.

Here's what to do next:

1. Fork the repository.
2. Create a new branch.
3. Make your changes.
4. Run the tests.
5. Push your changes.
6. Create a pull request.

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
pip install -r requirements/dev.txt
```

### Install the local version of Flask-Imp.

```bash
flit install
```

### Create a new app.

```bash
flask-imp init --name app --full
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
python3 tests_docker
```

### Type checking.

```bash
mypy
```

```bash
pyright
```

### Info

The tests are located in the `tests` folder.

The test Flask app is located in the `tests/test_app` folder.

The tests are linked to the `tests` blueprint located at `tests/test_app/blueprints/tests`.

### Building the docs.

All docs are generated from the [docs](docs) folder.

Edit these files, then run the following command to generate the docs.

```bash
flask --app docs compile
```

You can set it to watch for changes and automatically recompile the docs by adding the `--watch` flag.

```bash
flask --app gdocs compile --watch
```
