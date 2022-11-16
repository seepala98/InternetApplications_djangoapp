from django import forms
from myapp.models import Order, Product, Client, Category

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['client', 'product', 'num_units']
        widgets = {
            'client': forms.RadioSelect(),
        }
        labels = {
            'num_units': 'Quantity',
            'client': 'Client Name',
        }


class InterestForm(forms.Form):
    interested = forms.ChoiceField(choices=[(1, 'Yes'), (0, 'No')], widget=forms.RadioSelect)
    quantity = forms.IntegerField(min_value=1, initial=1)
    comments = forms.CharField(widget=forms.Textarea, label='Additional Comments', required=False)


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)

class RegisterForm(forms.ModelForm):

    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField(widget=forms.EmailInput)
    class Meta:
        model = Client
        fields = ['username', 'password', 'first_name', 'last_name', 'email', 'company', 'shipping_address', 'city',
                  'province']
        widgets = {
            'password': forms.PasswordInput(),
        }
        labels = {
            'username': 'Username',
            'password': 'Password',
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email',
            'company': 'Company',
            'shipping_address': 'Shipping Address',
            'city': 'City',
            'province': 'Province',
        }
        help_texts = {
            'username': 'Please enter your username',
        }
        error_messages = {
            'username': {
                'max_length': 'This username is too long',
            },
        }
        success_messages = {
            'username': {
                'max_length': 'This username is too long',
            },
        }