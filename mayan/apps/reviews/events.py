from django.utils.translation import ugettext_lazy as _

from mayan.apps.events.classes import EventTypeNamespace

namespace = EventTypeNamespace(label=_('Reviews'), name='reviews')


event_review_created = namespace.add_event_type(
    label=_('Review created'), name='review_created'
)
event_review_edited = namespace.add_event_type(
    label=_('Review edited'), name='review_edited'
)
event_review_document_added = namespace.add_event_type(
    label=_('Document added to review'), name='add_document'
)
event_review_document_removed = namespace.add_event_type(
    label=_('Document removed from review'), name='remove_document'
)
