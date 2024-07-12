from django.urls import path, include
from . import views

app_name = 'poteri'

urlpatterns = [
    path('', views.index, name = 'index' ),
    path('news/', views.news, name = 'news' ),
    path('schot/', views.schot, name = 'schot' ),
    path('<int:statia_id>', views.detal, name = 'detal'),
    path('pro_p/', views.Pro_p.as_view(), name = 'pro_p' ),
    path('<int:statia_id>/lave_comment', views.lave_comment, name = 'lave_comment'),
    path('schot/zadacha', views.zadacha, name = 'zadacha' ),
    path('schot2', views.Coins.as_view(), name = 'coins' ),
    path('schot/json_poteri', views.josn_poteri, name = 'josn_poteri'),
    path('coin_img', views.coin_img, name = 'coin_img' ),
    path('schot3', views.Trip.as_view(), name = 'trip' ),
    path('trip_img', views.trip_img, name = 'trip_img' )
]