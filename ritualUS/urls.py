"""
URL configuration for ritualUS project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from .views import Home, profile_view, ProductListView, ProductDetailView, contact, about, update_cart, cart_view, remove_from_cart, PaymentSuccessView, PaymentView, order_confirmation_view, confirmed_order, order_tracking_view, search_products


urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('profile/', profile_view, name='profile'),
    path('products/', ProductListView.as_view(), name='products'),
    path('cart/', cart_view, name='cart'),
    path('cart/update/', update_cart, name='update_cart'),
    path('cart/remove_product/', remove_from_cart, name='remove_from_cart'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('contact/', contact, name='contact'),
    path('about/', about, name='about'),
    path('payment/<int:order_id>/', PaymentView.as_view(), name='payment'),
    path('payment/success/<int:order_id>/',
         PaymentSuccessView.as_view(), name='payment_success'),
    path('order_confirmation/', order_confirmation_view,
         name='order_confirmation_view'),
    path('confirmed_order/', confirmed_order, name='confirmed_order'),
    path('order_tracking/', order_tracking_view, name='order_tracking'),
    path('search/', search_products, name='search_products'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATICFILES_DIRS)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
