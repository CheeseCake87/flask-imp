from app import create_app

if __name__ == '__main__':
    app = create_app("dev_config.toml")
    app.run()
else:
    wsgi = create_app("pro_config.toml")
