from django.urls import path
from . import views


app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('<int:pk>/test/', views.EditView.as_view(), name="test"),
    path('encounter/new/', views.AddEncounter.as_view(), name='add_encounter'),
    path('encounter/<int:pk>/', views.DetailEncounter.as_view(), name='detail_encounter'),
    path('encounter/<int:pk>/edit/', views.EditEncounter.as_view(), name='edit_encounter'),
    path('encounter/<int:pk>/delete/', views.DeleteEncounter.as_view(), name='delete_encounter'),
    path('encounters/', views.EncounterIndex.as_view(), name='encounters'),
]
