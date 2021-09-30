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
    link_review_view, link_review_edit, link_candidate_list, link_candidate_edit, link_candidate_delete,
    link_candidate_review_list
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
        Candidate = self.get_model(model_name='Candidate')
        # attach main links to menu component & add to main menu
        menu_reviews.bind_links(
            links=(
                link_review_list, link_review_create, link_candidate_list, link_candidate_create
            )
        )
        menu_main.bind_links(links=(menu_reviews,), position=96)
        # attach CRUD links to review object
        menu_object.bind_links(
            links=(
                link_review_delete, link_review_view, link_review_edit
            ), sources=(ReviewForm,)
        )
        # attach CRUD links to candidate object
        menu_object.bind_links(
            links=(
                link_candidate_delete, link_candidate_edit
            ), sources=(Candidate,)
        )
        menu_list_facet.bind_links(
            links=(
                link_candidate_review_list,
            ), sources=(Candidate,)
        )
        # attach info to review object (list_view)
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
        # attach info to candidate object (list_view)
        SourceColumn(
            attribute='firstName', is_identifier=False, is_sortable=True,
            source=Candidate
        )
        SourceColumn(
            attribute='lastName', is_identifier=False, is_sortable=True,
            source=Candidate
        )
        source_column_candidate_review_count = SourceColumn(
            func=lambda context: context['object'].get_reviews_count(), 
            include_label=True, label=_('Total Reviews'), source=Candidate
        )
        source_column_candidate_interview_avg = SourceColumn(
            func=lambda context: context['object'].get_reviews_interview_avg(),
            include_label=True, label=_('Avg Interview Score'), source=Candidate
        )
        source_column_candidate_leadership_avg = SourceColumn(
            func=lambda context: context['object'].get_reviews_leadership_avg(),
            include_label=True, label=_('Avg Leadership Score'), source=Candidate
        )
        source_column_candidate_recletter_avg = SourceColumn(
            func=lambda context: context['object'].get_reviews_recletter_avg(),
            include_label=True, label=_('Avg Rec Letters Score'), source=Candidate
        )
        source_column_candidate_extra_avg = SourceColumn(
            func=lambda context: context['object'].get_reviews_extra_avg(),
            include_label=True, label=_('Avg Extracurricular Score'), source=Candidate
        )
        source_column_candidate_essay_avg = SourceColumn(
            func=lambda context: context['object'].get_reviews_essay_avg(),
            include_label=True, label=_('Avg Essay Score'), source=Candidate
        )
 