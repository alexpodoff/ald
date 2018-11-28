"""Module for host-add command"""

import pytest
import subprocess
import shlex
from .ald_admin_data import valid_hostname_generator

__author__ = 'pod'
__version__ = '0.1'


@pytest.mark.parametrize('host', valid_hostname_generator())
def test_default_validname_host(ald_init, host, app):
    admpass = ald_init[0]
    app.host.create(host, admpass)
    hostget = "ald-admin host-get {host} -f --pass-file={pwd}"
    hostget = hostget.format(host=host, pwd=ald_init[1])
    sproc = subprocess.Popen(shlex.split(hostget),
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
    out, err = sproc.communicate()
    assert not err
    host_info = out.decode()
    assert host in host_info

