

__author__ = 'pod'
__version__ = '0.1'


def test_policy_del(ald_init, app):
    admpass = ald_init[0]
    passfile = ald_init[1]
    policy_list = app.policy.policy_list(passfile)
    if policy_list == ['default']:
        app.policy.create_policy('testpolicy', admpass)
    old_policy_list = app.policy.policy_list(passfile)
    policy = app.policy.random_policy_get(passfile)
    app.policy.policy_del(policy, admpass)
    new_policy_list = app.policy.policy_list(passfile)
    old_policy_list.remove(policy)
    assert new_policy_list == old_policy_list

