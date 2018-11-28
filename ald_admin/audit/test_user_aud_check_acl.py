

import pexpect
import os
import shutil
import errno
from socket import getfqdn, gethostname
from ald_admin.ald_admin_data import valid_name_generator
from fixture.params import aud_flags


def test_user_aud_check_acl(ald_init, app):
    admpass = ald_init[0]
    passfile = ald_init[1]
    aud_list = app.user.user_aud_list(passfile)
    user_list = app.user.user_list()
    user, u_passwd = valid_name_generator(), 'Testpass123'
    if user not in user_list:
        app.user.user_create(user, admpass, u_passwd)
    if user in str(aud_list):
        app.user.user_aud_del(user, admpass)
        app.user.user_aud_add(user, hex(aud_flags['acl']), hex(aud_flags['acl']), admpass)
    else:
        app.user.user_aud_add(user, hex(aud_flags['acl']), hex(aud_flags['acl']), admpass)

    app.user.user_ald_cap(user, getfqdn(), passfile)

    aud_dir = '/tmp/dir_for_test'
    aud_flag = 'setacl'

    try:
        os.mkdir(aud_dir, 0o700)
    except OSError as mkdir_err:
        if mkdir_err.errno == errno.EEXIST:
            shutil.rmtree(aud_dir)
            os.mkdir(aud_dir, 0o700)
        else:
            raise

    app.base.clean_kernel_mlog()
    user_uid = app.base.get_user_uid(user)

    usession = pexpect.spawnu('login %s' % user, timeout=3)
    usession.expect('Пароль:')
    usession.sendline(u_passwd)
    usession.expect(user + '@' + gethostname())
    usession.sendline('/usr/bin/setfacl -R -m u::rw %s' % aud_dir)
    usession.expect(user + '@' + gethostname())

    kern_list = app.base.kernlog_list(user_uid)

    result = app.user.user_aud_check(kern_list, call=aud_flag, obj=aud_dir, flag='[f]')
    assert result

    app.base.clean_kernel_mlog()
    os.chown(aud_dir, user_uid, user_uid)

    usession.sendline('/usr/bin/setfacl -R -d -m u::rw %s' % aud_dir)
    usession.expect(user + '@' + gethostname())
    usession.sendline('exit')
    usession.expect(pexpect.EOF)
    usession.close()
    assert usession.exitstatus == 0
    assert not usession.isalive()

    kern_list = app.base.kernlog_list(user_uid)
    result = app.user.user_aud_check(kern_list, call=aud_flag, obj=aud_dir, flag='[s]')
    assert result

    shutil.rmtree(aud_dir)
