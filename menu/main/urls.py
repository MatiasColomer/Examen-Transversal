from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.home, name='home'),
    path('save-cart/', views.save_cart, name='save_cart'),
    path('add_product/', views.add_product, name='add_product'),
    path('add_admin/', views.add_admin, name='add_admin'),
    path('view_purchases/', views.view_purchases, name='view_purchases'),
    path('save_purchase/', views.save_purchase, name='save_purchase'),
    path('view_all_purchases/', views.view_all_purchases, name='view_all_purchases'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)