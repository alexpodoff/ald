

import pexpect
import subprocess
from socket import getfqdn, gethostname
from fixture.params import aud_flags
from ald_admin.ald_admin_data import valid_name_generator


def test_user_aud_check_mount(ald_init, app):
    admpass = ald_init[0]
    passfile = ald_init[1]
    aud_list = app.user.user_aud_list(passfile)
    user_list = app.user.user_list()
    user, u_passwd = valid_name_generator(), 'Testpass123'
    if user not in user_list:
        app.user.user_create(user, admpass, u_passwd)
    if user in str(aud_list):
        app.user.user_aud_del(user, admpass)
        app.user.user_aud_add(user, hex(aud_flags['mount']), hex(aud_flags['mount']), admpass)
    else:
        app.user.user_aud_add(user, hex(aud_flags['mount']), hex(aud_flags['mount']), admpass)

    cap = 'cap_sys_admin'
    app.user.user_ald_cap(user, getfqdn(), passfile)

    aud_flag = 'mount'

    app.base.clean_kernel_mlog()
    user_uid = app.base.get_user_uid(user)

    usession = pexpect.spawnu('login %s' % user, timeout=3)
    usession.expect('Пароль:')
    usession.sendline(u_passwd)
    usession.expect(user + '@' + gethostname())
    usession.sendline('python3')
    usession.expect('>>>')
    usession.sendline('import ctypes')
    usession.expect('>>>')
    usession.sendline("libc = ctypes.CDLL('libc.so.6')")
    usession.sendline("libc.mount('/proc'.encode('ascii'), '/mnt'.encode('ascii'), 'proc'.encode('ascii'), 4096)")
    usession.expect('>>>')
    usession.sendline('exit()')
    usession.expect(user + '@' + gethostname())
    usession.sendline('exit')
    usession.expect(pexpect.EOF)
    usession.close()
    assert usession.exitstatus == 0
    assert not usession.isalive()

    kern_list = app.base.kernlog_list(user_uid)
    result = app.user.user_aud_check(kern_list, obj=None, call=aud_flag, flag='[f]')
    assert result

    app.user.user_linux_cap_mod(user, cap, admpass)

    usession = pexpect.spawnu('login %s' % user, timeout=3)
    usession.expect('Пароль:')
    usession.sendline(u_passwd)
    usession.expect(user + '@' + gethostname())
    usession.sendline('python3')
    usession.expect('>>>')
    usession.sendline('import ctypes')
    usession.expect('>>>')
    usession.sendline("libc = ctypes.CDLL('libc.so.6')")
    usession.sendline("libc.mount('/proc'.encode('ascii'), '/mnt'.encode('ascii'), 'proc'.encode('ascii'), 4096)")
    usession.sendline('exit()')
    usession.expect(user + '@' + gethostname())
    usession.sendline('exit')
    usession.expect(pexpect.EOF)
    usession.close()
    assert usession.exitstatus == 0
    assert not usession.isalive()

    kern_list = app.base.kernlog_list(user_uid)
    result = app.user.user_aud_check(kern_list, obj=None, call=aud_flag, flag='[s]')
    assert result

    subprocess.call('umount /mnt', shell=True)
