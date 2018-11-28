

__author__ = 'pod'
__version__ = '0.3'


def test_hgroup_del(ald_init, app):
    admpass = ald_init[0]
    default_hgroup_list = ['Domain Computers', 'Domain Controllers', 'Domain File Servers']
    hgroup_list = app.hgroup.hgroup_list()
    if hgroup_list == default_hgroup_list:
        app.hgroup.create('testhgroup', admpass)
    old_hgroup_list = app.hgroup.hgroup_list()
    hgroup = app.hgroup.random_hgroup_get()
    while hgroup in default_hgroup_list:
        hgroup = app.hgroup.random_hgroup_get()
    app.hgroup.hgroup_del(hgroup, admpass)
    new_hgroup_list = app.hgroup.hgroup_list()
    old_hgroup_list.remove(hgroup)
    assert new_hgroup_list == old_hgroup_list

