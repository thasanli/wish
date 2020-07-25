from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('registration', views.registration),
    path('wishes', views.user_profile),
    path('log_in', views.login),
    path('logout', views.logout),
    path('wishes/new', views.makeAwish),
    path('wishes/wish_submit', views.submit_wish),
    path('wishes/remove/<int:wish_id>', views.remove_wish),
    path('wishes/edit/<int:wish_id>', views.edit_wish),
    path('edit_wish/<int:wish_id>', views.edited_wish),
    path('granted/<int:wish_id>', views.granted_wish),
    path('wishes/stats', views.stats),
    path('wishes/liked/<int:grant_id>', views.liked),
]
