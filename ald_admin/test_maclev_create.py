"""Test module for ald-admin maclev-add command."""


from .ald_admin_data import valid_maclev_generator

__author__ = 'pod'
__version__ = '0.1'


def test_create_validname_maclev(ald_init, app):
    admpass = ald_init[0]
    maclev_list = app.macattr.maclev_list()
    maclev_count = len(maclev_list)
    maclev_need = (256 - maclev_count)
    while maclev_need != 0:
        numb = maclev_count
        maclev = valid_maclev_generator()
        app.macattr.maclev_create(numb, maclev, admpass)
        new_maclev = {numb: maclev}
        maclev_need -= 1
        maclev_count += 1
        maclev_list_new = app.macattr.maclev_list()
        maclev_list.update(new_maclev)
        assert maclev_list_new == maclev_list
