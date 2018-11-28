"""Test module for ald-admin maccat-add command."""

from .ald_admin_data import valid_maclev_generator

__author__ = 'pod'
__version__ = '0.1'


def test_create_validname_maccat(ald_init, app):
    admpass = ald_init[0]
    maccat_list = app.macattr.maccat_list()
    maccat_count = len(maccat_list)
    maccat_need = (64 - maccat_count)
    maccat_int = []
    # creates a list of 64 maccat hex values
    while maccat_need != 0:
        a = sum(maccat_int)
        maccat_int.append(a + 1)
        maccat_need -= 1
    maccat_hex_value = [hex(i) for i in maccat_int]
    # checking existing maccats and removing them from the list if found
    for cat in maccat_list:
        if cat in maccat_hex_value:
            maccat_hex_value.remove(cat)
    # creating random maccats till possible quantity of 64
    for cat in maccat_hex_value:
        name = valid_maclev_generator()
        app.macattr.maccat_create(cat, name, admpass)
        new_maccat = {cat: name}
        maccat_list_new = app.macattr.maccat_list()
        maccat_list.update(new_maccat)
        assert maccat_list_new == maccat_list
