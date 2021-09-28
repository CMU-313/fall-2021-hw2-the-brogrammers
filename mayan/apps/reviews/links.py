import copy

from django.utils.translation import ugettext_lazy as _

from mayan.apps.acls.links import link_acl_list
from mayan.apps.documents.permissions import permission_document_view
from mayan.apps.navigation.classes import Link
from mayan.apps.navigation.utils import get_cascade_condition

from .icons import (
    icon_review_list, icon_review_create, icon_review_edit, icon_review_delete, icon_candidate_create,
    icon_review_view
)

from .permissions import (
    permission_review_create, permission_review_view, permission_candidate_create
)

# Review Links
link_review_create = Link(
    icon=icon_review_create, permissions=(permission_review_create,),
    text=_('Create Review'), view='reviews:review_create'
)

link_review_list = Link(
    condition=get_cascade_condition(
        app_label='reviews', model_name='ReviewForm',
        object_permission=permission_review_view,
    ), icon=icon_review_list, 
    text=_('All'), view='reviews:review_list'
)

link_candidate_create = Link(
    icon=icon_candidate_create, permissions=(permission_candidate_create,),
    text=_('Create Candidate'), view='reviews:candidate_create'
)

# could potentially add permission to 2 below vv
link_review_delete = Link(
    args='object.pk', icon=icon_review_delete, 
    tags='dangerous', text=('Delete'), 
    view='reviews:review_delete'
)

link_review_view = Link(
    args='object.pk', icon=icon_review_view,
    text=_('Details'), view='reviews:review_detail'
)

link_review_edit = Link(
    args='object.pk', icon=icon_review_edit,
    text=_('Edit'), view='reviews:review_edit'
)