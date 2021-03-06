# [In-project modules]
from utils.kas_manager import get_kiuid_by_token, token_is_valid
from utils.database_operations import connect_to_database
# [Python native modules]
import logging
import random
# [Third-party modules]

logger = logging.getLogger(__name__)
class KiuidInfoError(Exception):
    pass
class ConstructSessionError(Exception):
    pass
class Session:
    def __init__(self, token = None, kiuid = None):
        """
        Session
        ===
        This class supports two ways of construction:

        ### One is:

        ```python
        session = Session(token = '...')
        ```
        This uses kas-account-token to construct.

        ### The other is:
        
        ```python
        session = Session(kiuid = '...')
        ```
        This uses kiuid directly to construct

        """
        if token != None and kiuid == None:
            self._kiuid = get_kiuid_by_token(token)
            if self._kiuid == None:
                raise KiuidInfoError('Invalid token!')
        elif kiuid != None:
            self._kiuid = kiuid
        else:
            raise ConstructSessionError('Invalid kiuid!')
        self._jobs = []
        self._debt = 0
        self._load_from_database()
        self.save()
        self.job_number = len(self._jobs)
        
    def has_job(self, code):
        return code in self._jobs

    def get_all_jobs(self):
        return [job for job in self._jobs]


    def remove_job(self, code):
        logger.debug("removing log: "+code)
        with connect_to_database() as connection:
            with connection.cursor() as cursor:
                cursor.execute('DELETE FROM print_codes WHERE code = %s;', (code, ))
        if self.has_job(code):
            # remove from the database
            self._jobs.remove(code)
            self.job_number -= 1
            logger.debug('Saving log...')
            self.save()
            logger.debug('Succeed; current codes: '+str(self._jobs))

    def _code_is_valid(self, code):
        is_valid = True

        with connect_to_database() as connection:
            with connection.cursor() as cursor:
                cursor.execute('SELECT code from print_codes where code = %s', (code, ))
                if cursor.fetchone() != None:
                    is_valid = False
        return is_valid
    def _generate_random_codes(self, length = 4):
        return ''.join([str(random.randint(0,9)) for _ in range(length)])
    def add_job(self):
        """
        This will generate a print task and updating it to the database.
        The final print code will be returned in the type of python string.
        """
        # generate four number in the format of string
        code = self._generate_random_codes()
        while not self._code_is_valid(code):
            code = self._generate_random_codes()
        
        # update code into database 
        with connect_to_database() as connection:
            with connection.cursor() as cursor:
                cursor.execute('INSERT INTO print_codes VALUES (%s, %s);', (code, self._kiuid))

        self._jobs.append(code)
        self.job_number += 1
        self.save()
        return code
        
    def get_kiuid(self):
        return self._kiuid

    def add_debt(self, value):
        self._debt += value
        self.save()
    def get_debt(self):
        return self._debt

    def remove_all_debt(self):
        self._debt = 0
        self.save()

    def save(self):
        with connect_to_database() as connection:
            with connection.cursor() as cursor:
                cursor.execute('SELECT kiuid FROM cp_sessions WHERE kiuid = %s;', (self._kiuid, ))
                if cursor.fetchone() == None:
                    # no such session yet
                    cursor.execute('INSERT INTO cp_sessions(kiuid, jobs, debt) VALUES (%s, %s, %s);', (self._kiuid, self._jobs, self._debt))
                else:
                    cursor.execute('UPDATE cp_sessions SET jobs = %s, debt = %s WHERE kiuid = %s;', (self._jobs, self._debt, self._kiuid))
    def _load_from_database(self):
        with connect_to_database() as connection:
            with connection.cursor() as cursor:
                cursor.execute('SELECT jobs,debt FROM cp_sessions WHERE kiuid = %s;', (self._kiuid, ))
                result = cursor.fetchone()
                if result != None:
                    logger.debug('Load: '+str(result))
                    # create a copy of the list
                    self._jobs = [i for i in result[0]] 
                    self._debt = result[1]
_sessions = {}

def get_session_by_code(code):
    with connect_to_database() as connection:
        with connection.cursor() as cursor:
            cursor.execute('SELECT kiuid from print_codes WHERE code = %s;', (code, ))
            result = cursor.fetchone()
            if result == None:
                return None
            result = result[0]
            return Session(kiuid = result)

def get_session_by_token(token):
    return Session(token = token)


def delete_session_status(token):
    """
    delete_session_status
    ===
    This deletes the relationship between a token->session key-value pair.
    This should be used as a cleanup
    """
    global _sessions
    _sessions.pop(token)

