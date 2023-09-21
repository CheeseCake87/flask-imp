```
Menu = CLI Commands/flask-imp init
Title = Initialising a Flask-Imp Project
```

Flask-Imp has a cli command that deploys a new ready-to-go project.
This project is structured in a way to give you the best idea of
how to use Flask-Imp.

## Create a new project

Make sure you are in the virtual environment, and at the root of your project folder, then run the following command:

```bash
flask-imp init
```

After running this command, you will be prompted to enter a name for your app:

```text
~ $ flask-imp init
What would you like to call your app? [app]: 
```

'app' is the default name, so if you just press enter, your app will be called 'app'. You will then see this output:

```text
===================
Flask app deployed!
===================
 
'/' route is set by the blueprint named www
found in the blueprints folder. It is encouraged
to use blueprints to set all app routes.
 
All app (non-blueprint) resources can be found
in the global folder. Have a look through this
folder to find out more.
 
Your app has the default name of 'app'
Flask will automatically look for this!
Run: flask run --debug
```

If you called your app something other than 'app', like 'new' for example, you will see:

```text
===================
Flask app deployed!
===================
 
'/' route is set by the blueprint named www
found in the blueprints folder. It is encouraged
to use blueprints to set all app routes.
 
All app (non-blueprint) resources can be found
in the global folder. Have a look through this
folder to find out more.
 
Your app has the name of 'new'
Run: flask --app new run --debug
```

As you can see from the output, it gives you instructions on how to start your app, depending on the name you gave it.

## init Folder structure

You should see a new folder that has been given the name you specified in
the `flask-imp init` command. 

This folder contains the following files and folders:

```text
app/
├── blueprints
│   └── www
│       ├── config.toml
│       ├── __init__.py
│       ├── routes
│       │   └── index.py
│       └── templates
│           └── www
│               └── index.html
│
├── extensions
│   └── __init__.py
│
├── global
│   ├── cli
│   │   └── cli.py
│   │
│   ├── context_processors
│   │   └── context_processors.py
│   │
│   ├── error_handlers
│   │   └── error_handlers.py
│   │
│   ├── filters
│   │   └── filters.py
│   │
│   ├── routes
│   │   └── routes.py
│   │
│   ├── static
│   │   ├── css
│   │   │   └── water.css
│   │   └── js
│   │       └── main.js
│   │
│   └── templates
│       ├── errors
│       │   ├── 400.html
│       │   ├── 401.html
│       │   ├── 403.html
│       │   ├── 404.html
│       │   ├── 405.html
│       │   └── 500.html
│       │
│       ├── extends
│       │   └── main.html
│       │
│       ├── includes
│       │   ├── footer.html
│       │   └── header.html
│       │
│       └── index.html
│
├── models
│   ├── example_user_table.py
│   └── __init__.py
│    
├── __init__.py
└── default.config.toml
```