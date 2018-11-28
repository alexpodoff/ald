
from .ald_admin_data import valid_maclev_generator

__author__ = 'pod'
__version__ = '0.1'


def test_maclev_mod(ald_init, app):
    """Modify random maclevel"""
    admpass = ald_init[0]
    passfile = ald_init[1]
    maclev_list = app.macattr.maclev_list()
    if len(maclev_list) == 1:
        app.macattr.maclev_create(1, "test_level", admpass)
    maclev = {0: ''}
    while 0 in maclev.keys():
        maclev = app.macattr.random_maclev_get()
    maclev = list(maclev.keys())[0]
    new_name = valid_maclev_generator()
    app.macattr.maclev_mod(maclev, new_name, passfile)
    new_maclev_list = app.macattr.maclev_list()
    maclev_list[maclev] = new_name
    assert new_maclev_list == maclev_list
