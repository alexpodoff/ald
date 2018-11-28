

import errno
import pexpect
import os
import shutil
import time
from socket import getfqdn
from fixture.params import aud_flags
from ald_admin.ald_admin_data import valid_name_generator


def test_user_aud_check_chmod(ald_init, app):
    admpass = ald_init[0]
    passfile = ald_init[1]
    aud_list = app.user.user_aud_list(passfile)
    user_list = app.user.user_list()
    user, u_passwd = valid_name_generator(), 'Testpass123'
    if user not in user_list:
        app.user.user_create(user, admpass, u_passwd)
    if user in str(aud_list):
        app.user.user_aud_del(user, admpass)
        app.user.user_aud_add(user, hex(aud_flags['chmod']), hex(aud_flags['chmod']), admpass)
    else:
        app.user.user_aud_add(user, hex(aud_flags['chmod']), hex(aud_flags['chmod']), admpass)

    app.user.user_ald_cap(user, getfqdn(), passfile)

    aud_dir = '/tmp/dir_for_test'
    aud_flag = 'chmod'

    app.base.clean_kernel_mlog()
    try:
        os.mkdir(aud_dir, 0o700)
    except OSError as mkdir_err:
        if mkdir_err.errno == errno.EEXIST:
            shutil.rmtree(aud_dir)
            os.mkdir(aud_dir, 0o700)
        else:
            raise

    user_uid = app.base.get_user_uid(user)
    os.chown(aud_dir, user_uid, user_uid)

    usession = pexpect.spawnu('login %s' % user, timeout=3)
    usession.expect('Пароль:')
    usession.sendline(u_passwd)
    usession.sendline('chmod 777 %s' % aud_dir)
    time.sleep(2)

    kern_list = app.base.kernlog_list(user_uid)

    result = app.user.user_aud_check(kern_list, obj=aud_dir, call=aud_flag, flag='[s]')
    # in case of the 1st fail
    if not result:
        usession.sendline('exit')
        usession.expect(pexpect.EOF)
        usession.close()
        assert usession.exitstatus == 0
        assert not usession.isalive()
    assert result

    os.chown(aud_dir, os.getuid(), os.getuid())
    app.base.clean_kernel_mlog()

    usession.sendline('chmod 777 %s' % aud_dir)
    usession.sendline('exit')
    usession.expect(pexpect.EOF)
    usession.close()
    assert usession.exitstatus == 0
    assert not usession.isalive()

    kern_list = app.base.kernlog_list(user_uid)
    result = app.user.user_aud_check(kern_list, obj=aud_dir, call=aud_flag, flag='[f]')
    assert result

    shutil.rmtree(aud_dir)
