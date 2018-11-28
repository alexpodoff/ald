"""test module for ald-admin policy-add command"""

import pytest
from .ald_admin_data import valid_usernames_generator

__author__ = 'pod'
__version__ = '0.1'


@pytest.mark.parametrize('policy', valid_usernames_generator())
def test_create_policy(ald_init, policy, app):
    admpass = ald_init[0]
    passfile = ald_init[1]
    app.policy.create_policy(policy, admpass)
    policy_info = app.policy.policy_info(policy, passfile)
    assert policy in policy_info
    assert '8' in policy_info
    assert '3' in policy_info
    assert '5' in policy_info
