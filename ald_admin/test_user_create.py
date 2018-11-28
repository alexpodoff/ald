"""Test module for ald-admin user-add command."""


import pytest
from .ald_admin_data import valid_usernames_generator, password_generator

__author__ = 'pod'
__version__ = '0.5.0'


@pytest.mark.parametrize('user', valid_usernames_generator())
def test_create_validname_user(ald_init, user, app):
    """Create user with all default settings."""
    user_password = password_generator()
    admpass = ald_init[0]
    passfile = ald_init[1]
    app.user.user_create(user, admpass, user_password)
    user_info = app.user.user_info(user, passfile)
    assert user in user_info
    assert 'Domain Users' in user_info
    assert 'audio, scanner, users, video' in user_info
    assert 'Тип ФС домашнего каталога: по умолчанию' in user_info
    assert '/ald_home/%s' % user in user_info
    assert '/bin/bash' in user_info
    assert '%s,,,' % user in user_info
    assert 'default' in user_info
    assert 'заблокирован: Нет' in user_info

