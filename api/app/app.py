from os import getenv
from dotenv import load_dotenv
from waitress import serve
from config import app


def start_app():
    load_dotenv()
    if getenv('ENVIRONMENT') == 'production':
        print('ENVIRONMENT', getenv('ENVIRONMENT'))
        serve(
            app,
            port=getenv('PORT'),
            host=getenv('HOST'),
        )
    else:
        app.run(
            debug=getenv('DEBUG'),
            port=getenv('PORT'),
            host=getenv('HOST'),
        )
