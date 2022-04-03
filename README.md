# Flask-Launchpad
A small auto importer for Flask blueprints and Apis

 - Auto imports blueprint routes and api routes (flask-restx)
 - Builtin folder contains some well used functions that you can pick and choose from

: Only currently compatable with linux OSs :

Create venv inside the flask_launchpad folder,  then install the requirements from the requirements.txt

It's recommended to run the app from the home folder of the user

Terminal:

cd /home/user/flask_launchpad

python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt

< remain in venv >

Run with : flask run :

export FLASK_APP=main
flask run

Run with : gunicorn :

- Accept connections from all IPs

gunicorn -b 0.0.0.0:5000 -w 3 run:app

- Accept connections only from localhost

gunicorn -b 127.0.0.1:5000 -w 3 run:app


