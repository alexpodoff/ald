

__author__ = 'pod'
__version__ = '0.2'


def test_user_del(ald_init, app):
    admpass = ald_init[0]
    user_list = app.user.user_list()
    if not user_list:
        app.user.user_create('testuser', admpass, 'Testpass123')
    old_user_list = app.user.user_list()
    user = app.user.random_user_get()
    app.user.user_del(user, admpass)
    new_user_list = app.user.user_list()
    old_user_list.remove(user)
    assert new_user_list == old_user_list

