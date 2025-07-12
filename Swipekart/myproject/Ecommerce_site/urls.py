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
    path('checkout/', views.checkout, name='checkout'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/add-address/', views.add_address, name='add_address'),
    path('profile/edit-address/<int:id>/', views.edit_address, name='edit_address'),
    path('profile/delete-address/<int:id>/', views.delete_address, name='delete_address'),
    path('checkout/', views.checkout, name='checkout'),
    path('place-order/', views.place_order, name='place_order'),
    path('order-success/<int:order_id>/', views.order_success, name='order_success'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('download-invoice/<int:order_id>/', views.download_invoice, name='download_invoice'),
]