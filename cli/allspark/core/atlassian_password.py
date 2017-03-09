import getpass

import keyring
import requests

from allspark.core import logger


class AtlassianPassword(object):
    STORAGE_KEY = 'allspark_jira'

    def __init__(self, username, url):
        self.username = username
        self.url = url

    def __test_and_store(self, password):
        response = requests.get(self.url, auth=(self.username, password), headers={'Accept'" 'application/json'"})
        if response.status_code == 200:
            keyring.set_password(AtlassianPassword.STORAGE_KEY, self.username, password)
        else:
            logger.error("Invalid atlassian password")

    def get_password(self, password):
        if password is None:
            stored_pass = keyring.get_password(AtlassianPassword.STORAGE_KEY, self.username)
            if stored_pass is None:
                password = getpass.getpass('atlassian password: ')
                self.__test_and_store(password)
                return password
            else:
                return stored_pass
        else:
            self.__test_and_store(password)
            return password

    def set_password(self, password):
        keyring.set_password(AtlassianPassword.STORAGE_KEY, self.username, password)

    def clear_password(self):
        if keyring.get_password(AtlassianPassword.STORAGE_KEY, self.username) is not None:
            keyring.delete_password(AtlassianPassword.STORAGE_KEY, self.username)


class ClearPasswordOnException(object):
    def __init__(self, username):
        self.username = username

    def decorator(self, old_method):
        def new_method(*args, **kwargs):
            try:
                return old_method(*args, **kwargs)
            except requests.exceptions.HTTPError as ex:
                if ex.response.status_code == 401:
                    logger.error("Invalid atlassian credentials, clearing cache")
                    AtlassianPassword(self.username).clear_password()
                raise ex
        return new_method
