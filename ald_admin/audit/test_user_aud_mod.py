"""Test module for user-aud-mod.
Sets audit flags on user, one at a time"""

import subprocess
from fixture.params import aud_flags
from ald_admin.ald_admin_data import valid_name_generator


def test_user_aud_mod(ald_init, app):
    admpass = ald_init[0]
    passfile = ald_init[1]
    subprocess.call('/etc/inid.d/aldd restart', shell=True)
    user, passwd = valid_name_generator(), 'Testpass123'
    app.user.user_create(user, admpass, passwd)
    app.user.user_aud_add(user, '0x1', '0x1', admpass)
    for flag in sorted(list(aud_flags.values()))[1:]:
        succ = fail = flag
        app.user.user_aud_mod(user, hex(succ), hex(fail), admpass)
        aud_list = app.user.user_aud_list(passfile)
        assert 'user:{0}: {1}:{2}'.format(user, hex(succ), hex(fail)) in aud_list
