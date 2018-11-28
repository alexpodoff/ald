

import socket

__author__ = 'pod'
__version__ = '0.1'


def test_hgroup_mod_hosts(ald_init, app):
    passfile = ald_init[1]
    admpass = ald_init[0]
    host_list = app.host.host_list()
    fqdn = socket.getfqdn()
    fqdn_list = []
    fqdn_list.append(fqdn)
    if host_list == fqdn_list:
        app.host.create('testhost', admpass)
    host = fqdn
    while host == fqdn:
        host = app.host.random_host_get()
    default_hgroup_list = ['Domain Computers', 'Domain Controllers', 'Domain File Servers']
    hgroup_list = app.hgroup.hgroup_list()
    if hgroup_list == default_hgroup_list:
        app.hgroup.create('testhgroup', admpass)
    hgroup = app.hgroup.random_hgroup_get()
    while hgroup in default_hgroup_list:
        hgroup = app.hgroup.random_hgroup_get()
    app.hgroup.hgroup_mod_hosts(hgroup, host, "add", passfile)
    hgroup_info = app.hgroup.hgroup_info(hgroup, passfile)
    assert hgroup in hgroup_info
    assert host in hgroup_info
    app.hgroup.hgroup_mod_hosts(hgroup, host, "rm", passfile)
    hgroup_info = app.hgroup.hgroup_info(hgroup, passfile)
    assert hgroup in hgroup_info
    assert host not in hgroup_info

