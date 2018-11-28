

import pytest
from .ald_admin_data import mac_level_invalid_generator, valid_maclev_generator

__author__ = 'pod'
__version__ = '0.1'


@pytest.mark.parametrize('level', mac_level_invalid_generator())
def test_user_maclev_mod(ald_init, level, app):
    admpass = ald_init[0]
    passfile = ald_init[1]
    maclev_list = app.macattr.maclev_list()
    user_list = app.user.user_list()
    if not user_list:
        app.user.user_create('testuser', admpass, 'Testpass123')
    user = app.user.random_user_get()
    min_level, max_level = level
    if min_level not in maclev_list:
        app.macattr.maclev_create(min_level, valid_maclev_generator(), admpass)
    if max_level not in maclev_list:
        app.macattr.maclev_create(max_level, valid_maclev_generator(), admpass)
    app.user.user_maclev_mod(user, min_level, max_level, passfile)
    user_full_info = app.user.user_full_info(user, passfile)
    assert user in user_full_info
    assert '(%s)' % str(min_level) not in user_full_info
    if max_level != 0:
        assert '(%s)' % str(max_level) not in user_full_info
