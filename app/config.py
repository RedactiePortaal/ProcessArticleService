import os

from dotenv import load_dotenv, find_dotenv

envLocation = find_dotenv()
load_dotenv(envLocation)

appConfig = {
    'neo4j': {
        'url': os.environ.get('NEO4J_URI'),
        'username': os.environ.get('NEO4J_USERNAME'),
        'password': os.environ.get('NEO4J_PASSWORD'),
    }
}
