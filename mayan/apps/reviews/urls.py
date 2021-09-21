### Application Routing File ###
from django.conf.urls import url
from .. import cabinets

urlpatterns = [
    url(
        # sample URL for the URL pattern, OBVIOUSLY you would link to a more
        # appropriate view!
        regex=r'^reviews/$', name='cabinet_list',
        view=cabinets.views.CabinetListView.as_view()
        )
]