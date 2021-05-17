from django.urls import path
from . import views

app_name = 'buddyfinder'
urlpatterns = [
    path('', views.index, name='index'),
    path('preferences/', views.get_preferences, name='preferences'),
    path('match/', views.get_matches, name='matching'),
    path('spotify/', views.spotify, name='spotify'),
    path('spotify2/', views.spotify2, name='spotify2'),
    path('messages/',views.get_inbox,name= 'inbox'),
    path('directs/<username>', views.get_directs, name='directs'),
    path('send/', views.send_direct, name='send_direct'),
    path('new/<username>', views.start_conversation, name='start_conversation')
]
