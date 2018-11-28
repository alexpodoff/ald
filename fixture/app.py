

import sys
import pexpect
from fixture.user import UserHelper
from fixture.hgroup import HGroupHelper
from fixture.policy import PolicyHelper
from fixture.host import HostHelper
from fixture.macattr import MacAttrHelper
from fixture.base import BaseHelper


class Application:

    def __init__(self):
        self.user = UserHelper(self)
        self.hgroup = HGroupHelper(self)
        self.policy = PolicyHelper(self)
        self.host = HostHelper(self)
        self.macattr = MacAttrHelper(self)
        self.base = BaseHelper(self)

    def ald_cmd(self, passfile=None):
        if passfile:
            adm = pexpect.spawnu('ald-admin cmd -f --pass-file=%s' % passfile, timeout=3)
        else:
            adm = pexpect.spawnu('ald-admin cmd', timeout=3)
        adm.logfile = sys.stdout
        matched = adm.expect(['>( |\t)', pexpect.EOF, pexpect.TIMEOUT])
        assert matched == 0
        return adm
