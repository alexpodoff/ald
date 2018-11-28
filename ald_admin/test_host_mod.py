

import socket
from fixture.params import modify_host as mh

__author__ = 'pod'
__version__ = '0.1'


def test_host_mod(ald_init, app):
    admpass = ald_init[0]
    passfile = ald_init[1]
    host_list = app.host.host_list()
    fqdn = socket.getfqdn()
    fqdn_list = []
    fqdn_list.append(fqdn)
    if host_list == fqdn_list:
        app.host.create('testhost', admpass)
    host = fqdn
    while host == fqdn:
        host = app.host.random_host_get()
    app.host.host_mod(host, passfile)
    host_info = app.host.host_info(host, passfile)
    assert host in host_info
    assert 'Описание: %s' % mh['host-desc'] in host_info
    assert 'Флаги: %s' % mh['host-flags'] in host_info
    assert 'Идентификатор (для сервера): %s' % mh['server-id'] in host_info

