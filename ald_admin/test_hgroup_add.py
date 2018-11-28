"""Module for hgroup-add command"""

import pytest
import subprocess
import shlex
from .ald_admin_data import valid_hgroupname_generator

__author__ = 'pod'
__version__ = '0.3.0'


@pytest.mark.parametrize('hgroup', valid_hgroupname_generator())
def test_default_validname_group(ald_init, hgroup, app):
    admpass = ald_init[0]
    app.hgroup.create(hgroup, admpass)
    hgroupget = "ald-admin hgroup-get {grp} -f --pass-file={pwd}"
    hgroupget = hgroupget.format(grp=hgroup, pwd=ald_init[1])
    sproc = subprocess.Popen(shlex.split(hgroupget),
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
    out, err = sproc.communicate()
    assert not err
    hgroup_info = out.decode()
    assert hgroup in hgroup_info
