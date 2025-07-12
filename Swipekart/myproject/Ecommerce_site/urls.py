from django.urls import path
from .import views



urlpatterns=[
    path('',views.home,name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout_view'),
    path('collections',views.collections,name='collections'),
    path('collections/<str:name>',views.collections_view,name='collections_view'),
    path('collections/<str:cname>/<str:pname>',views.product_details,name='product_details'),
    path('addtocart', views.add_to_cart, name='addtocart'),
    path('cart', views.cart_page, name='cart'),
    path('removeCart/<str:cid>', views.remove_cart, name='remove_cart'),

]