from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from Shared.DataAccess.config.docker_db import DockerDBConnection
from Shared.DataAccess.config.local_db import LocalDBConnection

engine = create_engine(
    f"mssql+pyodbc://{DockerDBConnection.USERNAME}:{DockerDBConnection.PASSWORD}@{DockerDBConnection.SERVER}/{DockerDBConnection.DATABASE}?driver={DockerDBConnection.DRIVER}"
    )

Session = sessionmaker(engine)
session = Session()