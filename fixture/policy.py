import random
import pexpect
import pytest
import subprocess
import shlex
import sys
from fixture.params import create_policy
from fixture.params import modify_policy
from fixture.params import del_policy


class PolicyHelper:

    def __init__(self, app):
        self.app = app

    def policy_list(self, passfile):
        policy_list = "ald-admin policy-list --pass-file=%s" % passfile
        sproc = subprocess.Popen(shlex.split(policy_list),
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
        out, err = sproc.communicate()
        plist = out.decode()
        return list(plist.split())

    def random_policy_get(self, passfile):
        policy_list = self.policy_list(passfile)
        with open('/tmp/dbg', 'w') as dbg:
            dbg.write(str(policy_list))
        policy_list.remove('default')
        policy = random.choice(policy_list)
        return policy

    def create_policy(self, policy, a_passwd):
        adm = self.app.ald_cmd()
        enter = adm.sendline
        adm.sendline('policy-add %s' % policy)
        # Put admin and new user passwords
        adm.expect(create_policy['01-padmin'])
        adm.sendline(a_passwd)
        for key in sorted(create_policy.keys())[1:]:
            adm.expect(create_policy[key])
            adm.sendline()
        adm.expect('> ')
        adm.sendline('exit')
        adm.expect(pexpect.EOF)
        adm.close()
        assert adm.exitstatus == 0
        assert not adm.isalive()

    def policy_info(self, policy, passfile):
        policyget = "ald-admin policy-get %s -f --pass-file=%s" % (policy, passfile)
        sproc = subprocess.Popen(shlex.split(policyget),
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
        out, err = sproc.communicate()
        assert not err
        return out.decode()

    def policy_mod(self, policy, passfile):
        adm = self.app.ald_cmd(passfile)
        for key in sorted(modify_policy):
            adm.sendline('policy-mod {0} --{1}={2}'.format(policy, key, modify_policy[key]))
            adm.expect("> ")
        adm.sendline('exit')
        adm.expect(pexpect.EOF)
        adm.close()
        assert adm.exitstatus == 0
        assert not adm.isalive()

    def policy_del(self, policy, a_passwd):
        adm = self.app.ald_cmd()
        adm.sendline('policy-rm %s' % policy)
        adm.expect(del_policy['01-padmin'])
        adm.sendline(a_passwd)
        adm.expect(del_policy['02-confirm'])
        adm.sendline("yes")
        adm.expect("> ")
        adm.sendline('exit')
        adm.expect(pexpect.EOF)
        adm.close()
        assert adm.exitstatus == 0
        assert not adm.isalive()

