from app import create_app

if __name__ == '__main__':
    app = create_app()
    app.run()
else:
    gunicorn = create_app()
