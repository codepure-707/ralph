#!/usr/bin/env bash

uv run dev_ralph shell -c """from ralph.accounts.models import RalphUser
from django.contrib.contenttypes.models import ContentType
from ralph.lib.transitions.tests.factories import TransitionFactory, TransitionModelFactory
from ralph.back_office.models import BackOfficeAsset

try:
    user = RalphUser.objects.create_superuser('admin', None, 'admin')
    print('Created superuser \'admin\' with password \'admin\'')
except:
    user = RalphUser.objects.get(username='admin')


transitions = [t for t in ['RETURN_TRANSITION_ID', 'LOAN_TRANSITION_ID', 'TRANSITION_ID']]
ct = ContentType.objects.get_for_model(BackOfficeAsset)
tm = TransitionModelFactory(content_type=ct)
tr = TransitionFactory(name='foo', model=tm, source=['in progress'],  target='in use')
print('Please make sure these lines are in your local settings:')
for transition in transitions:
    print(f'ACCEPT_ASSETS_FOR_CURRENT_USER_CONFIG[\'{transition}\'] = {tr.id}')
"""
