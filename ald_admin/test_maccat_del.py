

__author__ = 'pod'
__version__ = '0.1'


def test_maccat_del(ald_init, app):
    admpass = ald_init[0]
    maccat_list = app.macattr.maccat_list()
    if len(maccat_list) == 0:
        app.macattr.maccat_create(hex(1), "test_cat", admpass)
    maccat = app.macattr.random_maccat_get()
    maccat = list(maccat.keys())[0]
    app.macattr.maccat_del(maccat, admpass)
    new_maccat_list = app.macattr.maccat_list()
    for key in maccat_list.keys():
        if key == maccat:
            del maccat_list[key]
            break
    assert new_maccat_list == maccat_list
