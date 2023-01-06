import os

from pydantic import BaseSettings, Field
from dotenv import load_dotenv, find_dotenv

envLocation = find_dotenv()
load_dotenv(envLocation)


class Neo4j(BaseSettings):
    uri: str = Field(default="neo4j://localhost:7687", env="NEO4J_URI")
    username: str = Field(default="neo4j", env="NEO4J_USERNAME")
    password: str = Field(default="testtesttest", env="NEO4J_PASSWORD")


class Settings(BaseSettings):
    neo4j: Neo4j = Neo4j()
