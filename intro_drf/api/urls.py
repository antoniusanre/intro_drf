from .views import *
from django.urls import path

urlpatterns = [
    path('get-institution-trade', InstitutionsView.as_view(), name='get-institution-trade'),
    path('report', ReportsView.as_view(), name='report'),
    path('metadata', MetadataView.as_view(), name='metadata'),
]