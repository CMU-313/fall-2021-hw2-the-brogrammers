from django.apps import apps
from django.utils.translation import ugettext_lazy as _

from mayan.apps.acls.classes import ModelPermission
from mayan.apps.acls.permissions import permission_acl_edit, permission_acl_view
from mayan.apps.common.apps import MayanAppConfig
from mayan.apps.navigation.classes import SourceColumn
from mayan.apps.common.classes import ModelCopy, ModelQueryFields
from mayan.apps.common.menus import (
    menu_facet, menu_list_facet, menu_main, menu_multi_item, menu_object,
    menu_secondary
)
from .links import (
    link_review_list, link_review_create, link_candidate_create, link_review_delete,
    link_review_view, link_review_edit
)
from .menus import menu_reviews

# config info for app
class ReviewsApp(MayanAppConfig):
    app_namespace = 'reviews'
    app_url = 'reviews'
    has_rest_api = False
    has_tests = False
    name = 'mayan.apps.reviews'
    verbose_name = _('Reviews')
    def ready(self):
        super().ready()
        ReviewForm = self.get_model(model_name='ReviewForm')
        # attach links to menu component & add to main menu
        menu_reviews.bind_links(
            links=(
                link_review_list, link_review_create, link_candidate_create
            )
        )
        menu_main.bind_links(links=(menu_reviews,), position=96)
        # attach CRUD links to review object
        menu_object.bind_links(
            links=(
                link_review_delete, link_review_view, link_review_edit
            ), sources=(ReviewForm,)
        )
        # attach information to review object 
        SourceColumn(
            attribute='candidate', is_identifier=False, is_sortable=True,
            source=ReviewForm
        )
        SourceColumn(
            attribute='reviewerName', is_identifier=False, is_sortable=True,
            source=ReviewForm
        )
        SourceColumn(
            attribute='created_at', is_identifier=False, is_sortable=True,
            source=ReviewForm
        )
        
