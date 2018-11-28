"""Test modifies name and description of ald host group"""

from fixture.params import modify_hgroup as mh

__author__ = 'pod'
__version__ = '0.2'


def test_hgroup_mod(ald_init, app):
    admpass = ald_init[0]
    passfile = ald_init[1]
    default_hgroup_list = ['Domain Computers', 'Domain Controllers', 'Domain File Servers']
    hgroup_list = app.hgroup.hgroup_list()
    if hgroup_list == default_hgroup_list:
        app.hgroup.create('testhgroup', admpass)
    hgroup = app.hgroup.random_hgroup_get()
    while hgroup in default_hgroup_list:
        hgroup = app.hgroup.random_hgroup_get()
    app.hgroup.hgroup_mod(hgroup, passfile)
    hgroup = mh['name']
    hgroup_info = app.hgroup.hgroup_info(hgroup, passfile)
    assert hgroup in hgroup_info
    assert 'Описание: %s' % mh['hgroup-desc'] in hgroup_info

