"""Test module for user-aud-mod.
Sets random set of audit flags on user"""


import random
from fixture.params import aud_flags
from ald_admin.ald_admin_data import valid_name_generator


def test_user_aud_random(ald_init, app):
    admpass = ald_init[0]
    passfile = ald_init[1]
    aud_list = app.user.user_aud_list(passfile)
    user, passwd = valid_name_generator(), 'Testpass123'
    app.user.user_create(user, admpass, passwd)
    if user in str(aud_list):
        app.user.user_aud_del(user, admpass)
    count_succ = random.choice(range(1, 18))
    count_fail = random.choice(range(1, 18))
    succ = random.choice(list(aud_flags.values()))
    fail = random.choice(list(aud_flags.values()))
    while count_succ != 0:
        succ += random.choice(list(aud_flags.values()))
        count_succ -= 1
    while count_fail != 0:
        succ += random.choice(list(aud_flags.values()))
        count_fail -= 1
    app.user.user_aud_add(user, hex(succ), hex(fail), admpass)
    aud_list = app.user.user_aud_list(passfile)
    aud_list = [flag.lower() for flag in aud_list]
    assert 'user:{0}: {1}:{2}'.format(user, hex(succ), hex(fail)) in aud_list
