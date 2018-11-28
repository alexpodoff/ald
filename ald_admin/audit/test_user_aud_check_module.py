"""Test checks the success and fail audit of init and delete kernel module """

import pexpect
import subprocess
from socket import getfqdn, gethostname
from ald_admin.ald_admin_data import valid_name_generator
from fixture.params import aud_flags


def test_user_aud_check_module(ald_init, app):
    admpass = ald_init[0]
    passfile = ald_init[1]
    aud_list = app.user.user_aud_list(passfile)
    user_list = app.user.user_list()
    user, u_passwd = valid_name_generator(), 'Testpass123'
    if user not in user_list:
        app.user.user_create(user, admpass, u_passwd)
    if user in str(aud_list):
        app.user.user_aud_del(user, admpass)
        app.user.user_aud_add(user, hex(aud_flags['module']), hex(aud_flags['module']), admpass)
    else:
        app.user.user_aud_add(user, hex(aud_flags['module']), hex(aud_flags['module']), admpass)

    cap = 'cap_sys_module'
    app.user.user_ald_cap(user, getfqdn(), passfile)

    aud_flag_init = 'init_module'
    aud_flag_delete = 'delete_module'

    app.base.clean_kernel_mlog()
    user_uid = app.base.get_user_uid(user)

    usession = pexpect.spawnu('login %s' % user, timeout=3)
    usession.expect('Пароль:')
    usession.sendline(u_passwd)
    usession.expect(user + '@' + gethostname())
    usession.sendline('/sbin/modprobe evbug')
    usession.expect(user + '@' + gethostname())

    kern_list = app.base.kernlog_list(user_uid)

    result = app.user.user_aud_check(kern_list, call=aud_flag_init, flag='[f]')
    # in case of the 1st fail
    if not result:
        usession.sendline('exit')
        usession.expect(pexpect.EOF)
        usession.close()
        assert usession.exitstatus == 0
        assert not usession.isalive()
    assert result

    subprocess.call('/sbin/modprobe evbug', shell=True)

    usession.sendline('/sbin/modprobe -r evbug')
    usession.expect(user + '@' + gethostname())
    usession.sendline('exit')
    usession.expect(pexpect.EOF)
    usession.close()
    assert usession.exitstatus == 0
    assert not usession.isalive()

    kern_list = app.base.kernlog_list(user_uid)
    result = app.user.user_aud_check(kern_list, call=aud_flag_delete, flag='[f]')
    assert result

    app.user.user_linux_cap_mod(user, cap, admpass)
    subprocess.call('/sbin/modprobe -r evbug', shell=True)

    usession = pexpect.spawnu('login %s' % user, timeout=3)
    usession.expect('Пароль:')
    usession.sendline(u_passwd)
    usession.expect(user + '@' + gethostname())
    usession.sendline('/sbin/modprobe evbug')
    usession.expect(user + '@' + gethostname())

    kern_list = app.base.kernlog_list(user_uid)

    result = app.user.user_aud_check(kern_list, call=aud_flag_init, flag='[s]')
    # in case of the 1st fail
    if not result:
        usession.sendline('exit')
        usession.expect(pexpect.EOF)
        usession.close()
        assert usession.exitstatus == 0
        assert not usession.isalive()
    assert result

    usession.sendline('/sbin/modprobe -r evbug')
    usession.expect(user + '@' + gethostname())
    usession.sendline('exit')
    usession.expect(pexpect.EOF)
    usession.close()
    assert usession.exitstatus == 0
    assert not usession.isalive()

    kern_list = app.base.kernlog_list(user_uid)
    result = app.user.user_aud_check(kern_list, call=aud_flag_delete, flag='[s]')
    assert result
