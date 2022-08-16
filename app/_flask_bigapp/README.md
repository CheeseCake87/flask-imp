![](https://raw.githubusercontent.com/CheeseCake87/Flask-BigApp/master/app/structures/bigapp_default/static/img/Flask-BigApp-Logo-wbg1.png)
# Flask-BigApp

```bash
pip install flask-bigapp
```
## What is Flask-BigApp?

Flask-BigApp's main purpose is to help simplify the importing of blueprints, routes and models.

It has a few extra features built in to help with theming, securing pages and password authentication.

You can import model classes using `bigapp.import_models(file="models.py")`

You can auto import routes from a folder using `bigapp.import_builtins("folder that contains routes")`

You can auto import blueprints using `bigapp.import_blueprints("folder that contains blueprint modules")`

You can register a theme (structure) folder using `bigapp.import_structures("folder that containes themes(structures)")`


## GitHub

A full example project can be found on [github](https://github.com/CheeseCake87/Flask-BigApp)
