from django.urls import path
from . import views


app_name = 'npl'
urlpatterns = [
    path('', views.landing_page, name="landing_page"),
    path('features/', views.features, name="features"),
    path('contact/', views.contact, name="contact"),
    path('signup/', views.CreateUserView.as_view(), name='signup'),
    path('encounter/new/', views.new_encounter, name="new_encounter"),
    path('encounter/<int:pk>/', views.DetailEncounter.as_view(), name='detail_encounter'),
    path('encounter/<int:pk>/edit/', views.edit_encounter, name='edit_encounter'),
    #    path('encounter/<int:pk>/edit/', views.EditEncounter.as_view(), name='edit_encounter'),
    path('encounter/<int:pk>/delete/', views.DeleteEncounter.as_view(), name='delete_encounter'),
    path('my_encounters/list/', views.EncounterIndexList.as_view(), name='my_encounters'),
    path('my_encounters/map/', views.encounter_map, name='my_encounters_map'),
    path('dashboard/', views.view_my_dashboard, name='dashboard'),
    path('settings/', views.view_settings, name="settings"),
    path('team/<int:pk>/', views.view_team, name="team_detail"),
    path('team/<int:pk>/dashboard', views.view_team_dashboard, name="team_dashboard"),
    path('team/create_team/', views.create_team, name="create_team"),
    path('team/join_team/', views.join_team, name="join_team"),
    path('team/leave_team/<int:pk>', views.leave_team, name="leave_team"),
    path('login/', views.log_in, name="login"),
    path('logout/', views.log_out, name="logout"),
]

# path('team/<int:pk>/encounters/', views.TeamEncounters.as_view(), name="team_encounters"),
