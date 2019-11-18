"""
example usage
```python

with connect_to_database() as connection:
    with connection.cursor() as cursor:
        cursor.execute(...)
        cursor.fetchone()

```
"""
# [In-project modules]
from config import DatabaseConfig
# [Python native modules]
import logging
# [Third-party modules]
import psycopg2


db_logger = logging.getLogger(__name__)


class DatabaseConnection:
    """
    this is gives a database connection in with statement.
    
    """
    def __enter__(self):
        try:
            self._connection = psycopg2.connect(
                dbname = DatabaseConfig.database,
                user = DatabaseConfig.user, 
                host = DatabaseConfig.host, 
                password = DatabaseConfig.password, 
                port = DatabaseConfig.port
            )
            
        except Exception:
            db_logger.exception('Cannot connect to database')
        return self._connection
    def __exit__(self, type, value, traceback):
        if value != None:
            # an error occured; rollback
            db_logger.exception('An SQL error occured:  ')
            self._connection.rollback()
            # we leave the exception raised for the caller to deal with (according to Python's documentation: 3.3.9. With Statement Context Managers)
        self._connection.commit()
        self._connection.close()

def connect_to_database():
    return DatabaseConnection()

db_logger.info('Ready.')