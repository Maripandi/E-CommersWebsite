
from django.urls import path

from shop import views

urlpatterns = [
    path('',views.home,name='home'),
    path('reg',views.register, name='register'),
    path('collections',views.collections,name='collection'),
    path('collections/<str:name>',views.collectionview,name='collection'),
    path('collections/<str:cname>/<str:pname>',views.product_details,name='pdetails'),
    path('login',views.login_page,name='login'),
    path('logout',views.logout_page,name='logout'),
    path('addtocart',views.add_to_cart,name='addtocart'),
    path('cart',views.cart_page,name='cart'),
    path('rmvcart/<int:cid>',views.remove_cart, name='removecart'),
    path('fav_items',views.fav_items,name='fav'),
    path('fav_page',views.fav_page,name='favpage'),
    path('unfav/<int:fid>',views.un_fav,name='unfav'),
]
