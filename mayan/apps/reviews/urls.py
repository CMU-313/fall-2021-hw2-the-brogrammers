from django.conf.urls import url
from .. import cabinets
from . import views

# Review app routing
urlpatterns_review = [
    url(
        regex=r'^reviews/$', name='review_list',
        view=views.ReviewListView.as_view()
    ),
    url(
        regex=r'^reviews/create/$', name='review_create',
        view=views.ReviewCreateView.as_view()
    ),
    url(
        regex=r'^reviews/(?P<reviewform_id>\d+)/details/$',
        name='review_detail', view=views.ReviewDetailView.as_view()
    ),
    url(
        regex=r'^reviews/(?P<reviewform_id>\d+)/delete/$',
        name='review_delete', view=views.ReviewDeleteView.as_view()
    ),
    url(
        regex=r'^reviews/(?P<reviewform_id>\d+)/edit/$',
        name='review_edit', view=views.ReviewEditView.as_view()
    )
]

# Candidate routing
urlpatterns_candidate = [
    url(
        regex=r'^candidates/create/$', name='candidate_create',
        view=views.CandidateCreateView.as_view()
    ),
    url(
        regex=r'^candidates/$', name='candidate_list',
        view=views.CandidateListView.as_view()
    ),
    url(
        regex=r'^candidates/(?P<candidate_id>\d+)/edit/$',
        name='candidate_edit', view=views.CandidateEditView.as_view()
    ),
    url(
        regex=r'^candidates/(?P<candidate_id>\d+)/delete/$',
        name='candidate_delete', view=views.CandidateDeleteView.as_view()
    ),
    url(
        regex=r'^candidates/(?P<candidate_id>\d+)/reviews/$', name='candidate_review_list',
        view=views.CandidateReviewListView.as_view()
    )
]

urlpatterns = []
urlpatterns.extend(urlpatterns_review)
urlpatterns.extend(urlpatterns_candidate)