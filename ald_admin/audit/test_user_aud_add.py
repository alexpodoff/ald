
import random
from fixture.params import aud_flags


def test_user_aud_add(ald_init, app):
    admpass = ald_init[0]
    passfile = ald_init[1]
    user_list = app.user.user_list()
    aud_list = app.user.user_aud_list(passfile)
    if not user_list:
        app.user.user_create('testuser', admpass, 'Testpass123')
    user = app.user.random_user_get()
    if user in aud_list:
        app.user.user.aud_del(user, admpass)
    succ = random.choice(list(aud_flags.values()))
    fail = random.choice(list(aud_flags.values()))
    app.user.user_aud_add(user, hex(succ), hex(fail), admpass)
    aud_list = app.user.user_aud_list(passfile)
    assert 'user:{0}: {1}:{2}'.format(user, hex(succ), hex(fail)) in aud_list

    """
    for flag in aud_flags:
        suc = fail = flag
        app.user.user_aud_add(user, hex(succ), hex(fail), admpass)
        aud_list = app.user.user_aud_list()
        assert 'user:{0}: {1}:{2}'.format(user, hex(succ), hex(fail)) in aud_list
    """
