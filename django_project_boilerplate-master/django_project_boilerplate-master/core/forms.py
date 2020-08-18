from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

PAYMENT_CHOICES = (
    ('S','Stripe'),
    ('P','Paypal'),
    ('C','Cash-On-Delivery'),
    ('D','Debitcard'),
)
class CheckoutForm(forms.Form):
    #widget is django"s representation of an Html input element
    shipping_address = forms.CharField(required=False)
    shipping_address2  = forms.CharField(required=False)
    #formfiled functions gives the various countries option to select from
    shipping_country = CountryField(blank_label='(select country)').formfield(
        required=False,
        widget=CountrySelectWidget(attrs={
        'class':'custom-select d-block w-100'
    }))
    shipping_zip = forms.CharField(required=False)

    billing_address = forms.CharField(required=False)
    billing_address2  = forms.CharField(required=False)
    billing_country = CountryField(blank_label='(select country)').formfield(
        required=False,
        widget=CountrySelectWidget(attrs={
        'class':'custom-select d-block w-100'
    }))



    
    billing_zip = forms.CharField(required=False)

    same_billing_address = forms.BooleanField(required=False)
    set_default_shipping = forms.BooleanField(required=False)
    use_default_shipping = forms.BooleanField(required=False)
    set_default_billing = forms.BooleanField(required=False)
    use_default_billing = forms.BooleanField(required=False)
  
    payment_option = forms.ChoiceField(widget=forms.RadioSelect,choices=PAYMENT_CHOICES)



class CouponForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={
        'class' :'form-control',
        'placeholder':'Promo code',
        'aria-label':'Recipient \'s username',
        'aria-describedby':'basic-addon2',
    }))

    # \ is used for special charracters in dictionary data type

class RefundForm(forms.Form):
    ref_code = forms.CharField(help_text='Sent via Email during order confirmation')
    message =forms.CharField(widget= forms.Textarea(attrs={
        'row':3

    }))
    email =forms.EmailField()

class PaymentForm(forms.Form):
    stripeToken = forms.CharField(required=False)
    save = forms.BooleanField(required=False)
    use_default = forms.BooleanField(required=False)




from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# Sign Up Form
class MyCustomSignupForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='')
    last_name = forms.CharField(max_length=30, required=False, help_text='')
    email = forms.EmailField(max_length=254, help_text='Enter a valid Email address')

    class Meta:
        model = User
        fields = [
            'username', 
            'first_name', 
            'last_name', 
            'email', 
            'password1', 
            'password2', 
            ]

