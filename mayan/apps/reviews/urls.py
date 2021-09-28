### Application Routing File ###
from django.conf.urls import url
from .. import cabinets
from . import views

# Review app routing
urlpatterns = [
    url(
        regex=r'^reviews/$', name='review_list',
        view=views.ReviewListView.as_view()
    ),
    url(
        regex=r'^reviews/create/$', name='review_create',
        view=views.ReviewCreateView.as_view()
    ),
    url(
        regex=r'^candidate/create/$', name='candidate_create',
        view=views.CandidateCreateView.as_view()
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