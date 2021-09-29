from django.utils.translation import ugettext_lazy as _

from mayan.apps.navigation.classes import Menu
from mayan.apps.navigation.utils import get_cascade_condition

from .icons import icon_review_menu
from .permissions import permission_review_view, permission_review_create

# "Review" app menu component
menu_reviews = Menu(
    condition=get_cascade_condition(
        app_label='reviews', model_name='ReviewForm',
        object_permission=permission_review_view,
        view_permission=permission_review_create,
    ), icon=icon_review_menu, label=_('Reviews'), name='reviews'
)