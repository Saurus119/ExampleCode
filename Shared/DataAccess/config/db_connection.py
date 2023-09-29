import os

from .docker_db import DockerDBConnection
from .local_db import LocalDBConnection

class DBConnection:

    @staticmethod
    def create_db_conn_string() -> str:
        """Returns connection string for pyodb lib."""
        return (
            f'DRIVER={DockerDBConnection.DRIVER};'
            f'SERVER={DockerDBConnection.SERVER};'
            f'DATABASE={DockerDBConnection.DATABASE};'
            f'UID={DockerDBConnection.USERNAME};'
            f'PWD={DockerDBConnection.PASSWORD};'
        )
