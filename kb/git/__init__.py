# -*- coding: utf-8 -*-
"""
    kb
    ~~~~~~~~

    kb git package
"""

import json
import os
import subprocess
from flask import request, current_app as app
from ..settings import APP_REPOS, APP_FILES

class GitCommandErrorException(Exception):
    def __init__(self, out, error, *args, **kwargs):
        self.out = out
        self.error = error
        super(GitCommandErrorException, self).__init__(*args, **kwargs)

class MissingPayloadParam(Exception):
    pass

class InvalidPayloadParam(Exception):
    pass


def receive_hook():
    try:
        payload = ''
        branch = 'master'

        try:
            payload = request.json

        except KeyError, e:
            raise MissingPayloadParam()

        except Exception, e:
            raise InvalidPayloadParam()

        git = GitUpdater(Repository(payload['repository']))
        git.update()

        return 'OK', 200

    except MissingPayloadParam, e:
        return 'Missing payload data.', 403

    except InvalidPayloadParam, e:
        return 'Invalid Payload parameter received', 400

    except Exception, e:
        app.logger.error(e)
        return 'Something went wrong\n {stack}'.format(stack=e), 500


class Repository(object):
    def __init__(self, json_dict):
        super(Repository, self).__init__()
        self.name = json_dict['name']
        self.clone_url = json_dict['clone_url']
        self.branch = 'master'
        self.git_exec_path = '/usr/bin/'

    @property
    def path(self):
        return os.path.join(APP_REPOS, self.name)

    @property
    def file_path(self):
        return os.path.join(APP_FILES, self.name)

    @property
    def pull_command(self):
        str_command = '{git_exec_path}git pull origin {branch}'.format(**self.__dict__)
        app.logger.debug(str_command)
        return str_command

    @property
    def clone_command(self):
        str_command = '{git_exec_path}git clone {clone_url}'.format(**self.__dict__)
        app.logger.debug(str_command)
        return str_command

    def exists(self):
        return os.path.exists(self.path)

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)


class GitUpdater(object):
    def __init__(self, repo):
        self.git_exec_path = '/usr/bin/'
        self.repo = repo

        app.logger.debug('Affected branch: {0} on repo {1} at {2}'.format(repo.branch, repo, repo.path))

    def exec_command(self, command, cwd):
        pr = subprocess.Popen(command,
           cwd = cwd,
           shell = True,
           stdout = subprocess.PIPE,
           stderr = subprocess.PIPE
           )

        (out, error) = pr.communicate()
        app.logger.info("Out : " + str(error))
        app.logger.info("Out : " + str(out))
        if 'Error' in error or 'fatal' in error:
            raise GitCommandErrorException(out, error)

    def create_files_dir(self):
        try:
            os.mkdir(self.repo.file_path)
        except OSError:
            pass

    def update(self):
        if self.repo.exists():
            self.exec_command(self.repo.pull_command, self.repo.path)
        else:
            self.exec_command(self.repo.clone_command, APP_REPOS)
        self.create_files_dir()

