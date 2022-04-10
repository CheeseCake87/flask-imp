from main import create_app

if __name__ == '__main__':
    create_app(live=False).run()
else:
    flask_launchpad = create_app(live=True)
