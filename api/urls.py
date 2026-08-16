from django.urls import path
from .views import *

urlpatterns = [
    path('product/', Get_product.as_view(),),
    path('food/', Get_food.as_view(),),
    path('room/', get_rooms),
    path('create-order/', create_order),
    path('create-delivery/', create_delivery),
    path('info/', get_info),
    path('detail/', get_detail),
]
