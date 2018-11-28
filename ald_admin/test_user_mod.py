

from fixture.params import modify_user as mu

__author__ = 'pod'
__version__ = '0.5.0'


def test_user_mod(ald_init, app):
    """Create user with all default settings."""
    admpass = ald_init[0]
    passfile = ald_init[1]
    user_list = app.user.user_list()
    policy_list = app.policy.policy_list(passfile)
    if not user_list:
        app.user.user_create('testuser', admpass, 'Testpass123')
    if policy_list == ['default']:
        app.policy.create_policy('testpolicy', admpass)
    user = app.user.random_user_get()
    policy = app.policy.random_policy_get(passfile)
    app.user.user_mod(user, passfile, policy)
    user_info = app.user.user_info(user, passfile)
    assert user in user_info
    assert 'Описание: %s' % mu['user-desc'] in user_info
    assert 'Тип ФС домашнего каталога: %s' % mu['home-type'] in user_info
    assert 'Домашний каталог: %s' % mu['home'] in user_info
    assert 'Командная оболочка: %s' % mu['login-shell'] in user_info
    assert 'Поле gecos: %s' % mu['gecos'] in user_info
    assert 'Полное имя: %s' % mu['full-name'][1:-1] in user_info
    assert 'Политика: %s' % policy
