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
    SingleObjectDeleteView, SingleObjectEditView, SingleObjectListView,
    SingleObjectDetailView
)
from mayan.apps.views.mixins import ExternalObjectViewMixin
from .forms import ReviewDetailForm
from .permissions import (
    permission_review_create, permission_review_view, permission_candidate_create
)
from .models import ReviewForm, Candidate
from .icons import (
    icon_review_menu
)
from .links import (
    link_review_create
)

logger = logging.getLogger(name=__name__)


class CandidateCreateView(SingleObjectCreateView):
    fields = ('firstName', 'lastName', 'email', 'phone_number', 'gpa', 'major', 'university')
    model = Candidate
    post_action_redirect = reverse_lazy(viewname='reviews:review_create')
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
            'hide_link': True,
            'hide_object': True,
            'title' : _('Finished Reviews'),
            'no_results_icon': icon_review_menu,
            'no_results_main_link' : link_review_create.resolve(
                context=RequestContext(request=self.request)
            ),
            'no_results_text': _(
                'Reviews are a tiered method to aggregate '
                'information. Each review contains information '
                'on a specific candidate.'
            ),
            'no_results_title': _('No reviews available'),
        }

    def get_source_queryset(self):
        return ReviewForm.objects.root_nodes()

class ReviewDetailView(SingleObjectDetailView):
    form_class = ReviewDetailForm
    object_permission = permission_review_view
    pk_url_kwarg = 'reviewform_id' 

    def get_extra_context(self):
        return {
            'form_hide_help_text': True,
            'hide_labels': False,
            'object': self.object,
            'title': _('%s') % self.object,
        }

    def get_initial(self):
        return {
            'Reviewer Name': self.object.get_rendered_body("reviewerName"),
            'Candidate Name': self.object.get_rendered_body("candidate")
        }

    def get_source_queryset(self):
        return ReviewForm.objects.root_nodes()

class ReviewEditView(SingleObjectEditView):
    fields = ('candidate', 'reviewerName', 'leadership', 'extracurriculars', 'recLetters', 'interview', 'essay')
    model = ReviewForm
    # could add edit permission right here!
    post_action_redirect = reverse_lazy(viewname='reviews:review_list')
    pk_url_kwarg = 'reviewform_id'

    def get_extra_context(self):
        return {
            'object': self.object,
            'title': _('Edit Review: %s') % self.object,
        }

    def get_instance_extra_data(self):
        return {'_event_actor': self.request.user }

class ReviewDeleteView(SingleObjectDeleteView):
    model = ReviewForm
    # could do permission_delete!
    post_action_redirect = reverse_lazy(viewname='reviews:review_list')
    pk_url_kwarg = 'reviewform_id'

    def get_extra_context(self):
        return {
            'object' : self.object,
            'title': _('Delete the Review: %s?') % self.object,
        }
