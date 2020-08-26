from django.urls import path ,include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from .views import (HomeView,
ItemDetailView,
CheckoutView,
add_to_cart,
remove_from_cart,
OrderSummaryView,
remove_single_item_from_cart,
PaymentView,
AddCouponView,
RequestRefundView,
MyCustomSignupForm,
add_to_wishlist,
remove_from_wishlist,
WishlistSummaryView,
ShopAllView,
ShopView,
)
from django.views.generic import TemplateView

app_name = 'core'
#when a class based view is called use the as.view func
urlpatterns = [
    path('',HomeView.as_view(), name='home'),
    path('checkout/',CheckoutView.as_view(), name='checkout'),
    path('order-summary/',OrderSummaryView.as_view(), name='order-summary'),
    path('product/<slug>/',ItemDetailView.as_view(), name='product'),
    path('add-to-cart/<slug>/',add_to_cart, name='add-to-cart'),
    path('add-coupon/', AddCouponView.as_view(), name='add-coupon'),
    path('remove-from-cart/<slug>/',remove_from_cart, name='remove-from-cart'),
    path('remove-item-from-cart/<slug>/', remove_single_item_from_cart,
         name='remove-single-item-from-cart'),
         #here slug as payment_option which would select the payment option that was selected by the user
    path('payment/<payment_option>/',PaymentView.as_view(), name='payment'),
    path('request-refund/',RequestRefundView.as_view(), name='request-refund'),
    path ('signup/',MyCustomSignupForm.as_view(),name='signup'),
    path('wishlist-summary/',WishlistSummaryView.as_view(), name='wishlist-summary'),
    path('add_to_wishlist/<slug>/',add_to_wishlist, name='add_to_wishlist'),
    path('remove_from_wishlist/<slug>/',remove_from_wishlist, name='remove_from_wishlist'),
    path('contact/', 
    TemplateView.as_view(template_name='contact.html'),
    name='contact'),
    path('shop-all/',ShopAllView.as_view(), name='shop-all'),
    path('shop/clothing/',ShopView.as_view(), name='clothing'),
    path('shop/clothing/shawls/',ShopView.as_view(), name='shawls'),
    path('shop/clothing/gowns/',ShopView.as_view(), name='gowns'),
    path('shop/clothing/scarfs/',ShopView.as_view(), name='scarfs'),
    path('shop/decor/',ShopView.as_view(), name='decor'),
    path('shop/foods/',ShopView.as_view(), name='foods'),
    path('shop/foods/saffron/',ShopView.as_view(), name='saffron'),
    path('shop/foods/honey/',ShopView.as_view(), name='honey'),
    path('shop/foods/tea/',ShopView.as_view(), name='tea'),
    path('shop/foods/dryfruits/',ShopView.as_view(), name='dryfruits'),
    
]
#purana kaam
if settings.DEBUG:
      import debug_toolbar
      urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
      urlpatterns +=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
      urlpatterns +=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

