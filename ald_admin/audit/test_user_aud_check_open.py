

import errno
import pexpect
import os
import time
from socket import getfqdn
from fixture.params import aud_flags
from ald_admin.ald_admin_data import valid_name_generator


def test_user_aud_check_open(ald_init, app):
    admpass = ald_init[0]
    passfile = ald_init[1]
    aud_list = app.user.user_aud_list(passfile)
    user_list = app.user.user_list()
    user, u_passwd = valid_name_generator(), 'Testpass123'
    if user not in user_list:
        app.user.user_create(user, admpass, u_passwd)
    if user in str(aud_list):
        app.user.user_aud_del(user, admpass)
        app.user.user_aud_add(user, hex(aud_flags['open']), hex(aud_flags['open']), admpass)
    else:
        app.user.user_aud_add(user, hex(aud_flags['open']), hex(aud_flags['open']), admpass)

    app.user.user_ald_cap(user, getfqdn(), passfile)

    aud_dir = '/tmp/dir_for_test'
    aud_file = aud_dir + '/file_for_test'
    aud_flag = 'open'

    app.base.clean_kernel_mlog()
    try:
        os.mkdir(aud_dir, 0o700)
    except OSError as mkdir_err:
        if mkdir_err.errno == errno.EEXIST:
            os.chmod(aud_dir, 0o700)
            if os.access(aud_file, os.F_OK):
                os.remove(aud_file)
        else:
            raise
    with open(aud_file, 'w', encoding='utf-8') as audfile:
        audfile.write('test')
    os.chmod(aud_file, 0o700)

    user_uid = app.base.get_user_uid(user)
    os.chown(aud_file, user_uid, os.getuid())
    os.chown(aud_dir, user_uid, os.getuid())

    usession = pexpect.spawnu('login %s' % user, timeout=3)
    usession.expect('Пароль:')
    usession.sendline(u_passwd)
    usession.sendline('cat %s' % aud_file)
    time.sleep(2)

    kern_list = app.base.kernlog_list(user_uid)

    result = app.user.user_aud_check(kern_list, obj=aud_file, call=aud_flag)
    # in case of the 1st fail
    if not result:
        usession.sendline('exit')
        usession.expect(pexpect.EOF)
        usession.close()
        assert usession.exitstatus == 0
        assert not usession.isalive()
    assert result

    app.base.clean_kernel_mlog()

    os.chmod(aud_file, 0o070)
    usession.sendline('cat %s' % aud_file)
    usession.sendline('exit')
    usession.expect(pexpect.EOF)
    usession.close()
    assert usession.exitstatus == 0
    assert not usession.isalive()

    kern_list = app.base.kernlog_list(user_uid)
    result = app.user.user_aud_check(kern_list, obj=aud_file, call=aud_flag, flag='[f]')
    assert result
