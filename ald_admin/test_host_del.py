

import socket

__author__ = 'pod'
__version__ = '0.2'


def test_host_del(ald_init, app):
    admpass = ald_init[0]
    host_list = app.host.host_list()
    fqdn = socket.getfqdn()
    fqdn_list = []
    fqdn_list.append(fqdn)
    if host_list == fqdn_list:
        app.host.create('testhost', admpass)
    old_host_list = app.host.host_list()
    host = fqdn
    while host == fqdn:
        host = app.host.random_host_get()
    app.host.host_del(host, admpass)
    new_host_list = app.host.host_list()
    old_host_list.remove(host)
    assert new_host_list == old_host_list

