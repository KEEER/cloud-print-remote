# [In-project modules]
from utils.kas_info_manager import get_kiuid_by_token, token_is_valid
from utils.database_operations import connect_to_database
# [Python native modules]
import logging
# [Third-party modules]

logger = logging.getLogger(__name__)
class KiuidInfoError(Exception):
    pass
class Session:
    def __init__(self, token):
        self._kiuid = get_kiuid_by_token(token)
        if self._kiuid == None:
            raise KiuidInfoError('Invalid token!')
        self._jobs = []
        self._load_jobs_from_database()
        self.save()
        self.job_number = len(self._jobs)
        
    def has_job(self, code):
        return code in self._jobs

    def remove_job(self, code):
        if self.has_job(code):
            self._jobs.remove(code)
            self.job_number -= 1
            self.save()

    def add_job(self, code):
        self._jobs.append(code)
        self.job_number += 1
        self.save()

    def save(self):
        with connect_to_database() as connection:
            with connection.cursor() as cursor:
                cursor.execute('SELECT kiuid FROM cp_sessions WHERE kiuid = %s', (self._kiuid, ))
                if cursor.fetchone() == None:
                    # no such session yet
                    cursor.execute('INSERT INTO cp_sessions(kiuid, jobs) VALUES (%s, %s)', (self._kiuid, self._jobs))
    def _load_jobs_from_database(self):
        with connect_to_database() as connection:
            with connection.cursor() as cursor:
                cursor.execute('SELECT jobs FROM cp_sessions WHERE kiuid = %s', (self._kiuid, ))
                result = cursor.fetchone()
                if result != None:
                    # create a copy of the list
                    self._jobs = [i for i in result[0]]
    def __del__(self):
        self.save()
_sessions = {}


def get_session_by_token(token):
    global _sessions
    if not token in _sessions:
        if token_is_valid(token):
            new_session = Session(token)
            _sessions.update({token: new_session})
            return new_session
    else:
        return _sessions.get(token)

def delete_session_status(token):
    """
    delete_session_status
    ===
    This deletes the relationship between a token->session key-value pair.
    This should be used as a cleanup
    """
    global _sessions
    _sessions.pop(token)

