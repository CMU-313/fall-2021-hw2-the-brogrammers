from django.utils.translation import ugettext_lazy as _

from mayan.apps.permissions import PermissionNamespace

namespace = PermissionNamespace(label=_('Reviews'), name='reviews')

# Review permissions
permission_review_create = namespace.add_permission(
    label=_('Create Review'), name='review_create'
)

permission_review_view = namespace.add_permission(
    label=_('View Reviews'), name='review_view'
)

permission_candidate_create = namespace.add_permission(
    label=_('Create Candidate'), name='candidate_create'
)

permission_candidate_view = namespace.add_permission(
    label=_('View Candidates'), name='candidate_view'
)