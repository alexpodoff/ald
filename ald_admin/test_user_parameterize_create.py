"""Test module for ald-admin user-add command with certain parameters."""


import pwd
from fixture.params import create_user_parametrize as cup
from .ald_admin_data import valid_name_generator, password_generator

__author__ = 'pod'
__version__ = '0.2'


def test_create_validname_user(ald_init, app):
    """Create user with all default settings."""
    user = valid_name_generator()
    user_password = password_generator()
    policy = valid_name_generator()
    admpass = ald_init[0]
    passfile = ald_init[1]
    user_list = app.user.user_list()
    app.policy.create_policy(policy, admpass)
    if not user_list:
        xid = '2600'
    else:
        xid_list = []
        for u in user_list:
            xid_list.append(pwd.getpwnam(u)[2])
        xid = sorted(xid_list)[-1] + 1
    app.user.user_create_parametrize(user, str(xid), policy, admpass, user_password)
    user_info = app.user.user_full_info(user, passfile)
    assert user in user_info
    assert 'Описание: %s' % cup['user-desc'] in user_info
    assert 'Тип ФС домашнего каталога: %s' % cup['home-type'] in user_info
    assert 'Домашний каталог: %s' % cup['home'] in user_info
    assert 'Командная оболочка: %s' % cup['login-shell'] in user_info
    assert 'Поле gecos: %s' % cup['gecos'] in user_info
    assert 'Полное имя: %s' % cup['full-name'][1:-1] in user_info
    assert 'Политика: %s' % policy in user_info
    assert 'Первичная группа: %s' % cup['group'] in user_info
    assert 'Идентификатор (UID): %s' % xid in user_info
    assert 'Идентификатор (GID): %s' % xid in user_info
    assert 'Флаг принудительной смены пароля: Да' in user_info
