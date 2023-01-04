import os

from pydantic import BaseSettings, Field
from dotenv import load_dotenv, find_dotenv

envLocation = find_dotenv()
load_dotenv(envLocation)


class Neo4j(BaseSettings):
    uri: str = Field(env="NEO4J_URI")
    username: str = Field(env="NEO4J_USERNAME")
    password: str = Field(env="NEO4J_PASSWORD")


class Settings(BaseSettings):
    neo4j: Neo4j = Neo4j()
