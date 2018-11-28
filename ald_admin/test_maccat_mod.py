from .ald_admin_data import valid_maclev_generator

__author__ = 'pod'
__version__ = '0.1'


def test_maccat_mod(ald_init, app):
    """Modify random maclevel"""
    admpass = ald_init[0]
    passfile = ald_init[1]
    maccat_list = app.macattr.maccat_list()
    if maccat_list == {}:
        app.macattr.maccat_create(hex(1), "test_cat", admpass)
    maccat = app.macattr.random_maccat_get()
    maccat = list(maccat.keys())[0]
    new_name = valid_maclev_generator()
    app.macattr.maccat_mod(maccat, new_name, passfile)
    new_maccat_list = app.macattr.maccat_list()
    maccat_list[maccat] = new_name
    assert new_maccat_list == maccat_list
