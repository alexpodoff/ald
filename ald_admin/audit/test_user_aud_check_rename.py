

import errno
import pexpect
import os
import shutil
import time
from socket import getfqdn
from ald_admin.ald_admin_data import valid_name_generator
from fixture.params import aud_flags


def test_user_aud_check_rename(ald_init, app):
    admpass = ald_init[0]
    passfile = ald_init[1]
    aud_list = app.user.user_aud_list(passfile)
    user_list = app.user.user_list()
    user, u_passwd = valid_name_generator(), 'Testpass123'
    if user not in user_list:
        app.user.user_create(user, admpass, u_passwd)
    if user in str(aud_list):
        app.user.user_aud_del(user, admpass)
        app.user.user_aud_add(user, hex(aud_flags['rename']), hex(aud_flags['rename']), admpass)
    else:
        app.user.user_aud_add(user, hex(aud_flags['rename']), hex(aud_flags['rename']), admpass)

    app.user.user_ald_cap(user, getfqdn(), passfile)

    aud_dir = '/tmp/dir_for_test'
    aud_file = aud_dir + '/file_for_test'
    aud_flag = 'rename'

    app.base.clean_kernel_mlog()
    try:
        os.mkdir(aud_dir, 0o500)
    except OSError as mkdir_err:
        if mkdir_err.errno == errno.EEXIST:
            shutil.rmtree(aud_dir)
            os.mkdir(aud_dir, 0o500)
        else:
            raise

    with open(aud_file, 'w', encoding='utf-8') as audfile:
        audfile.write('test')

    user_uid = app.base.get_user_uid(user)
    os.chown(aud_file, os.getuid(), os.getuid())
    os.chown(aud_dir, user_uid, os.getuid())

    usession = pexpect.spawnu('login %s' % user, timeout=3)
    usession.expect('Пароль:')
    usession.sendline(u_passwd)
    usession.sendline('mv %s %s.bak' % (aud_file, aud_file))
    time.sleep(2)

    kern_list = app.base.kernlog_list(user_uid)

    result = app.user.user_aud_check(kern_list, call=aud_flag, obj=aud_file, flag='[f]')
    # in case of the 1st fail
    if not result:
        usession.sendline('exit')
        usession.expect(pexpect.EOF)
        usession.close()
        assert usession.exitstatus == 0
        assert not usession.isalive()
    assert result

    app.base.clean_kernel_mlog()

    os.chmod(aud_dir, 0o700)
    usession.sendline('mv %s %s.bak' % (aud_file, aud_file))
    usession.sendline('exit')
    usession.expect(pexpect.EOF)
    usession.close()
    assert usession.exitstatus == 0
    assert not usession.isalive()

    kern_list = app.base.kernlog_list(user_uid)
    result = app.user.user_aud_check(kern_list, call=aud_flag, obj=aud_file, flag='[s]')
    assert result

    shutil.rmtree(aud_dir)
