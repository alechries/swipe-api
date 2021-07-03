from django.urls import path
from . import views


urlpatterns = [
    path('apartment/', views.ApartmentList.as_view(), name='advertisement-list'),
    path('apartment/<int:pk>/', views.ApartmentDetail.as_view(), name='advertisement-detail'),
    path('floor/create/', views.FloorCreate.as_view(), name='floor-create'),
    path('auth/', views.auth)
    # path('house/', views.HouseList.as_view(), name='house-list'),
    # path('house/<int:pk>', views.HouseDetail.as_view(), name='house-detail'),
]
