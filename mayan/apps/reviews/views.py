### Application Views File ###
import logging

from django.template import RequestContext
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from mayan.apps.acls.models import AccessControlList
from mayan.apps.documents.models import Document
from mayan.apps.documents.views.document_views import DocumentListView
from mayan.apps.views.generics import (
    MultipleObjectFormActionView, SingleObjectCreateView,
    SingleObjectDeleteView, SingleObjectEditView, SingleObjectListView
)
from mayan.apps.views.mixins import ExternalObjectViewMixin

from .permissions import (
    permission_review_create, permission_review_view, permission_candidate_create
)
from .models import ReviewForm, Candidate
from .icons import icon_review_menu
from .links import (
    link_review_create 
)

logger = logging.getLogger(name=__name__)


class CandidateCreateView(SingleObjectCreateView):
    fields = ('firstName', 'lastName', 'email', 'phone_number', 'gpa', 'major', 'university')
    model = Candidate
    post_action_redirect = reverse_lazy(viewname='reviews:review_list')
    view_permission = permission_candidate_create
    def get_extra_context(self):
        return {
            'title':_('Create Candidate'),
        }
    
    def get_instance_extra_data(self):
        return {'_event_actor' : self.request.user }

class ReviewCreateView(SingleObjectCreateView):
    fields = ('candidate', 'reviewerName', 'leadership', 'extracurriculars', 'recLetters', 'interview', 'essay')
    model = ReviewForm
    post_action_redirect = reverse_lazy(viewname='reviews:review_list')
    view_permission = permission_review_create

    def get_extra_context(self):
        return {
            'title':_('Review Candidate'),
        }
    
    def get_instance_extra_data(self):
        return {'_event_actor' : self.request.user }

class ReviewListView(SingleObjectListView):
    object_permission = permission_review_view

    def get_extra_context(self):
        return {
            # could add hide things?
            'title' : _('Completed Reviews'),
            'no_results_icon' : icon_review_menu,
            'no_results_main_link' : link_review_create.resolve(
                context=RequestContext(request=self.request)
            ),
            'no_results_text' : _(
                'Review forms are used to score a candidate across multiple domains.'
            ),
            'no_results_title': _('No reviews completed yet'),
        }

    def get_source_queryset(self):
        return ReviewForm.get_reviews()
