### Application Routing File ###
from django.conf.urls import url
from .. import cabinets
from . import views

# Review app routing
urlpatterns = [
    url(
        regex=r'^create/$', name='review_create',
        view=views.ReviewCreateView.as_view()
    ),
    url(
        regex=r'^reviews/$', name='review_list',
        view=views.ReviewListView.as_view()
    )
]