```
Menu = CLI Commands/flask-imp init
Title = Initialising a Flask-Imp Project
```

Flask-Imp has a cli command that deploys a new ready-to-go project.
This project is structured in a way to give you the best idea of
how to use Flask-Imp.

```bash
flask-imp init --help
```

## Create a new project

Make sure you are in the virtual environment, and at the root of your project folder, then run the following command:

```bash
flask-imp init
```

After running this command, you will be prompted to choose what type of app you want to deploy:

```text
~ $ flask-imp init
What type of app would you like to create? (full, slim, minimal) [full]:
```

See below for the differences between the app types.

After this, you will be prompted to enter a name for your app:

```text
~ $ flask-imp init
What would you like to call your app? [app]: 
```

'app' is the default name, so if you just press enter, your app will be called 'app'. You will then see this output:

```text
===================
Flask app deployed!
===================
 
Your app has the default name of 'app'
Flask will automatically look for this!
Run: flask run --debug

```

If you called your app something other than 'app', like 'new' for example, you will see:

```text
===================
Flask app deployed!
===================

Your app has the name of 'new'
Run: flask --app new run --debug

```

As you can see from the output, it gives you instructions on how to start your app, depending on the name you gave it.

You should see a new folder that has been given the name you specified in
the `flask-imp init` command.

### Additional options

You can also specify a name for your app in the command itself, like so:

```bash
flask-imp init -n my_app
```

This will create a new app called 'my_app'.

You can also deploy a slim app, that will have one blueprint and no models, like so:

```bash
flask-imp init -n my_app --slim
```

You can also deploy a minimal app, that will have no blueprints, models, or extensions, like so:

```bash
flask-imp init -n my_app --minimal
```

## init Folder structures

### Full app

`flask-imp init`:

```text
app/
├── blueprints
│   └── www
│       ├── config.toml
│       ├── __init__.py
│       ├── routes
│       │   └── index.py
│       ├── static
│       │   ├── css
│       │   │   └── water.css
│       │   ├── img
│       │   │   └── flask-imp-logo.png
│       │   └── js
│       │       └── main.js
│       └── templates
│           └── www
│               ├── extends
│               │   └── main.html
│               ├── includes
│               │   ├── footer.html
│               │   └── header.html
│               └── index.html
│
├── extensions
│   └── __init__.py
│
├── resources
│   ├── cli
│   │   └── cli.py
│   ├── context_processors
│   │   └── context_processors.py
│   ├── error_handlers
│   │   └── error_handlers.py
│   ├── filters
│   │   └── filters.py
│   ├── routes
│   │   └── routes.py
│   ├── static
│   │   └── favicon.ico
│   └── templates
│       ├── errors
│       │   ├── 400.html
│       │   ├── 401.html
│       │   ├── 403.html
│       │   ├── 404.html
│       │   ├── 405.html
│       │   └── 500.html
│       └── index.html
│
├── models
│   ├── example_user_table.py
│   └── __init__.py
│
├── __init__.py
└── default.config.toml
```

### Slim app

`flask-imp init --slim`:

```text
app/
├── extensions
│   └── __init__.py
│
├── resources
│   ├── cli
│   │   └── cli.py
│   ├── error_handlers
│   │   └── error_handlers.py
│   ├── static
│   │   └── favicon.ico
│   └── templates
│       └── errors
│           ├── 400.html
│           ├── 401.html
│           ├── 403.html
│           ├── 404.html
│           ├── 405.html
│           └── 500.html
│
├── www
│   ├── config.toml
│   ├── __init__.py
│   ├── routes
│   │   └── index.py
│   ├── static
│   │   ├── css
│   │   │   └── water.css
│   │   ├── img
│   │   │   └── flask-imp-logo.png
│   │   └── js
│   │       └── main.js
│   └── templates
│       └── www
│           ├── extends
│           │   └── main.html
│           ├── includes
│           │   ├── footer.html
│           │   └── header.html
│           └── index.html
│
├── __init__.py
└── default.config.toml
```

### Minimal app

`flask-imp init --minimal`:

```text
app/
├── extensions
│   └── __init__.py
│
├── resources
│   ├── static
│   │   ├── css
│   │   │   └── water.css
│   │   ├── img
│   │   │   └── flask-imp-logo.png
│   │   └── favicon.ico
│   ├── templates
│   │   └── index.html
│   └── routes.py
│
├── __init__.py
└── default.config.toml
```
