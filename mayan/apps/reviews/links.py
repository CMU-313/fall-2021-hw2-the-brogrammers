import copy

from django.utils.translation import ugettext_lazy as _

from mayan.apps.acls.links import link_acl_list
from mayan.apps.documents.permissions import permission_document_view
from mayan.apps.navigation.classes import Link
from mayan.apps.navigation.utils import get_cascade_condition

from .icons import (
    icon_review_list, icon_review_create, icon_review_edit, icon_review_delete
)

from .permissions import (
    permission_review_create, permission_review_view
)

# Review Links
link_review_create = Link(
    icon=icon_review_create, permissions=(permission_review_create,),
    text=_('Create Review'), view='reviews:review_create'
)

link_review_list = Link(
    icon=icon_review_list, permissions=(permission_review_view,),
    text=_('All'), view='reviews:review_list'
)