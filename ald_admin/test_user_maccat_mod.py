

import pytest
from .ald_admin_data import mac_cat_combinations_generator, valid_maclev_generator

__author__ = 'pod'
__version__ = '0.1'


@pytest.mark.parametrize('cat', mac_cat_combinations_generator())
def test_user_maccat_mod(ald_init, cat, app):
    admpass = ald_init[0]
    passfile = ald_init[1]
    maccat_list = app.macattr.maccat_list()
    user_list = app.user.user_list()
    if not user_list:
        app.user.user_create('testuser', admpass, 'Testpass123')
    user = app.user.random_user_get()
    min_cat, max_cat = cat
    if hex(min_cat) != '0x0' and hex(min_cat) not in maccat_list:
        app.macattr.maccat_create(hex(min_cat), valid_maclev_generator(), admpass)
        maccat_list = app.macattr.maccat_list()
    if hex(max_cat) not in maccat_list:
        app.macattr.maccat_create(hex(max_cat), valid_maclev_generator(), admpass)
    app.user.user_maccat_mod(user, hex(min_cat), hex(max_cat), passfile)
    user_full_info = app.user.user_full_info(user, passfile)
    assert user in user_full_info
    assert '(%s)' % str(hex(min_cat)) in user_full_info
    assert '(%s)' % str(hex(max_cat)) in user_full_info
