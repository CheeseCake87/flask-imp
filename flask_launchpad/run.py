from main import create_app

main = create_app()

if __name__ == '__main__':
    main.run(host="localhost", port=5000)
