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
MyCustomSignupForm
)

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
    path ('signup/',MyCustomSignupForm.as_view(),name='signup')

]
#purana kaam
#if settings.DEBUG:
     # import debug_toolbar
      #urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
     # urlpatterns +=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
     # urlpatterns +=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

