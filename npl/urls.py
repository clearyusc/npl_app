from django.urls import path
from . import views


app_name = 'npl'
urlpatterns = [
    path('new/', views.add_encounter, name="add_encounter"),
    path('<int:pk>/', views.DetailEncounter.as_view(), name='detail_encounter'),
    path('<int:pk>/edit/', views.EditEncounter.as_view(), name='edit_encounter'),
    path('<int:pk>/delete/', views.DeleteEncounter.as_view(), name='delete_encounter'),
    path('encounters/', views.EncounterIndex.as_view(), name='encounters'),
]
