from django.urls import path
from .views import SourceListView, API_ConfigView, SolveView


urlpatterns = [
    path('', SourceListView.as_view(), name='quiz_list'),
    path('source/<slug:source_slug>/<int:pk>/config/', API_ConfigView.as_view(), name='api_config'),
    path('source/<slug:source_slug>/solve/', SolveView.as_view(), name="source_solve")
]

