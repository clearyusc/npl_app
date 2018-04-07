from django.urls import path
from . import views


app_name = 'npl'
urlpatterns = [
    path('encounter/new/', views.new_encounter, name="new_encounter"),
    path('encounter/<int:pk>/', views.DetailEncounter.as_view(), name='detail_encounter'),
    path('encounter/<int:pk>/edit/', views.edit_encounter, name='edit_encounter'),
    #    path('encounter/<int:pk>/edit/', views.EditEncounter.as_view(), name='edit_encounter'),
    path('encounter/<int:pk>/delete/', views.DeleteEncounter.as_view(), name='delete_encounter'),
    path('my_encounters/list/', views.EncounterIndexList.as_view(), name='my_encounters'),
    path('my_encounters/map/', views.encounter_map, name='my_encounters_map'),
    path('dashboard/', views.view_dashboard, name='dashboard'),
    path('settings/', views.Settings.as_view(), name="settings")
]

# path('team/<int:pk>/encounters/', views.TeamEncounters.as_view(), name="team_encounters"),
