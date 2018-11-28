"""This module contains fixtures for ALD tests."""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import pytest
import shutil
import shlex
import subprocess
from ald_admin.ald_admin_data import password_generator
from fixture.app import Application

__author__ = 'pod'
__version__ = '0.4'


@pytest.fixture
def app(request):
    fixture = Application()
    return fixture

def clean_dirs(export_dir):
    """If export_dir isn't empty then remove all subdirectories."""
    contain = os.listdir(export_dir)
    count = 0
    if contain:
        for home in contain:
            if os.path.isfile(home):
                continue
            shutil.rmtree(os.path.join(export_dir, home))
            count += 1
    return count


@pytest.fixture(scope='session')
def ald_init(request):
    """Initialize and destroy ALD databases. Return admin/admin password."""
    shutil.rmtree('/root/.ald')
    admin_admin = password_generator()
#    admin_admin = '1'
#    km = '1'
    km = password_generator()
    passwd = '/tmp/ald-passwd'
    with open(passwd, 'w') as pwd:
        pwd.write("admin/admin:{a}\nK/M:{k}\n".format(a=admin_admin, k=km))
    os.chmod(passwd, 0o0600)
    init = "ald-init init --force --pass-file={}".format(passwd)
    subprocess.check_output(shlex.split(init))
    return admin_admin, passwd

    def ald_destroy():
        """This finalizer destroys ALD databases."""
        destroy = "ald-init destroy --force --pass-file={}".format(passwd)
        subprocess.check_output(shlex.split(destroy))
        os.remove(passwd)
        clean_dirs('/ald_export_home')
        shutil.rmtree('/var/lib/ald/cache')

    request.addfinalizer(ald_destroy)
    return admin_admin, passwd

