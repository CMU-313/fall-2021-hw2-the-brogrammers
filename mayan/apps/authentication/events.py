from django.utils.translation import ugettext_lazy as _

from mayan.apps.events.classes import EventTypeNamespace

namespace = EventTypeNamespace(
    label=_('Authentication'), name='authentication'
)

event_user_impersonation_ended = namespace.add_event_type(
    label=_('User impersonation ended'), name='user_impersonation_ended'
)
event_user_impersonation_started = namespace.add_event_type(
    label=_('User impersonation started'), name='user_impersonation_started'
)
event_user_logged_in = namespace.add_event_type(
    label=_('User logged in'), name='user_logged_in'
)
event_user_logged_out = namespace.add_event_type(
    label=_('User logged out'), name='user_logged_out'
)
