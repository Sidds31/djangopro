"""
URL configuration for registration project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from demo1 import views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from django.views.static import serve
urlpatterns = [
    path("admin/", admin.site.urls),
    path('',views.signupPage,name='login'),
    path('login/',views.loginPage,name='otp'),
    path('home/',views.homePage,name='home'),
    path('search/',views.search,name='search'),
    path("category/<slug:val>",views.CategoryView.as_view(),name='category'),
    path("product_detail/<int:pk>",views.ProductDetail.as_view(),name='product-detail'),
    path('add-to-cart/',views.add_to_cart, name = 'add-to-cart'),
    path('cart/', views.show_cart, name= 'showcart'),
    path('checkout/',views.checkout.as_view(), name='checkout'),
    path('pluscart/',views.plus_cart),
    path('minuscart/',views.minus_cart),
    path('removecart/',views.remove_cart),
    path('prints/',views.prints),
    url(r'^media/(?P<path>.*)$', serve,{'document_root':       settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
