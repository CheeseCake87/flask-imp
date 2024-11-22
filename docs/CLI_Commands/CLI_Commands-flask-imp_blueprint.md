# Generate a Flask-Imp Blueprint

Flask-Imp has its own type of blueprint. It comes with some methods to auto import routes, and models etc... see
[ImpBlueprint-Introduction](../ImpBlueprint/ImpBlueprint-Introduction.md) for more information.

You have the option to generate a regular template rendering blueprint, or a API blueprint that returns a JSON response.

```bash
flask-imp blueprint --help
```
or
```bash
flask-imp api-blueprint --help
```

To generate a Flask-Imp blueprint, run the following command:

```bash
flask-imp blueprint
```
or
```bash
flask-imp api-blueprint
```

After running this command, you will be prompted to enter the location of where you want to create your blueprint:

```text
~ $ flask-imp blueprint
(Creation is relative to the current working directory)
Folder to create blueprint in [Current Working Directory]:
```

As detailed in the prompt, the creation of the blueprint is relative to the current working directory. So to create a
blueprint in the folder `app/blueprints`, you would enter `app/blueprints` in the prompt.

```text
~ $ flask-imp blueprint
(Creation is relative to the current working directory)
Folder to create blueprint in [Current Working Directory]: app/blueprints
```

You will then be prompted to enter a name for your blueprint:

```text
~ $ flask-imp blueprint
...
Name of the blueprint to create [my_new_blueprint]:
```

The default name is 'my_new_blueprint', we will change this to 'admin'

```text
~ $ flask-imp blueprint
...
Name of the blueprint to create [my_new_blueprint]: admin
```

After creating your blueprint, the folder structure will look like this:

```text
app/
├── blueprints
│   └── admin
│       ├── routes
│       │   └── index.py
│       │
│       ├── static
│       │   ├── css
│       │   │   └── water.css
│       │   ├── img
│       │   │   └── flask-imp-logo.png
│       │   └── js
│       │       └── main.js
│       │
│       ├── templates
│       │   └── www
│       │       ├── extends
│       │       │   └── main.html
│       │       ├── includes
│       │       │   ├── footer.html
│       │       │   └── header.html
│       │       └── index.html
│       │
│       └── __init__.py
│
...
```

This is a self-contained blueprint, so it has its own static, templates and routes folders.
You can now navigate '/admin'

You can streamline this process by specifying the name of the blueprint, the folder to
create it in and the configuration to use, like so:

```bash
flask-imp blueprint -n admin -f app/blueprints
```

