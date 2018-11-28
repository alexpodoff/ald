

import pwd
import subprocess
import shlex


class BaseHelper:

    def __init__(self, app):
        self.app = app

    def kernlog_list(self, object=None):
        """
        Returns the list of lines in kernel.mlog output;
        If object is set - returns kernlog | grep object
        :param object: str
        :return: list
        """
        kernlog_list = '/bin/bash -c kernlog'
        obj_list = 'grep %s' % object
        sproc1 = subprocess.Popen(shlex.split(kernlog_list),
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
        if object:
            sproc2 = subprocess.Popen(shlex.split(obj_list),
                                     stdin=sproc1.stdout,
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE)
            sproc1.stdout.close()
            out, err = sproc2.communicate()
        else:
            out, err = sproc1.communicate()
        kernlist = out.decode()
        kernlist = list(kernlist.split('\n'))[:-1]
        return kernlist

    def clean_kernel_mlog(self):
        """Clean parsec kernel.mlog."""
        with open('/var/log/parsec/kernel.mlog', 'w') as kernmlog:
            kernmlog.write('')

    def getent_passwd(self):
        """
        Returns list of getent passwd output
        :return: list
        """
        getent_passwd = 'getent passwd'
        sproc = subprocess.Popen(shlex.split(getent_passwd),
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
        out, err = sproc.communicate()
        passwd_list = out.decode()
        return list(passwd_list.split('\n'))

    def getent_group(self):
        """
        Returns list of getent group output
        :return: list
        """
        getent_passwd = 'getent group'
        sproc = subprocess.Popen(shlex.split(getent_passwd),
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
        out, err = sproc.communicate()
        passwd_list = out.decode()
        return list(passwd_list.split('\n'))

    def get_user_uid(self, user):
        """
        Returns user's UID
        :param user: str
        :return: int
        """
        return pwd.getpwnam(user)[2]
