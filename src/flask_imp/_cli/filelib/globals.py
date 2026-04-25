def globals_py(secret_key: str) -> str:
    return f"""\
#
# In this file you can store global variables that are used in your application.
# It is also a good idea to use python-dotenv with os.getenv here.
# pip install python-dotenv
#
# from os import getenv
# from dotenv import load_dotenv
#
# load_dotenv()
#

# !!! MOVE secret_key TO .env FILE
FLASK_SECRET_KEY = "{secret_key}"
# FLASK_SECRET_KEY = getenv("FLASK_SECRET_KEY")
"""
