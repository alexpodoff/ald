

__author__ = 'pod'
__version__ = '0.1'


def test_maclev_del(ald_init, app):
    admpass = ald_init[0]
    maclev_list = app.macattr.maclev_list()
    if len(maclev_list) == 1:
        app.macattr.maclev_create(1, "test_level", admpass)
    maclev = {0: ''}
    while 0 in maclev.keys():
        maclev = app.macattr.random_maclev_get()
    maclev = list(maclev.keys())[0]
    app.macattr.maclev_del(maclev, admpass)
    new_maclev_list = app.macattr.maclev_list()
    for key in maclev_list.keys():
        if key == maclev:
            del maclev_list[key]
            break
    assert new_maclev_list == maclev_list
