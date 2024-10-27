from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import *
from django import forms

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['fname','lname','username', 'email', 'password1', 'password2']
        widgets = {
            'fname':forms.TextInput(attrs={'class':'form-control'}),
            'lname':forms.TextInput(attrs={'class':'form-control'}),
            'username':forms.TextInput(attrs={'class':'form-control'}),
            'email':forms.EmailInput(attrs={'class':'form-control'}),
        }

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar','fname','lname','Contact','Address']
        widgets = {
            'avatar':forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'fname': forms.TextInput(attrs={'class': 'form-control'}),
            'lname': forms.TextInput(attrs={'class': 'form-control'}),
            'Contact': forms.NumberInput(attrs={'class': 'form-control'}),
            'Address': forms.TextInput(attrs={'class': 'form-control'}),
}
        

class ShopForm(ModelForm):
    class Meta:
        model = Shops
        fields = ['validids','banner','logo','shop_name','tin','brn','contact','email','address','shop_description','latitude', 'longitude']
        widgets = {
            'validids':forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'banner':forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'logo':forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'shop_name': forms.TextInput(attrs={'class': 'form-control'}),
            'tin': forms.TextInput(attrs={'class': 'form-control'}),
            'brn': forms.TextInput(attrs={'class': 'form-control'}),
            'contact': forms.NumberInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'shop_description': forms.Textarea(attrs={'class': 'form-control'}),
            'latitude': forms.HiddenInput(),
            'longitude': forms.HiddenInput(),
            
}
        

class VehicleForm(ModelForm):
    class Meta:
        model = Vehicle
        fields = ['documents','img1','img2','img3','img4','img5', 'categories', 'transmission', 'seat','fuels', 'color_description', 'model_car', 'plate', 'chasis_number', 'vin_no', 'vehicle_type','rent_per_hr']
        widgets = {
            'documents': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'img1': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'img2': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'img3': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'img4': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'img5': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'categories': forms.Select(attrs={'class': 'form-control'}),
            'transmission': forms.Select(attrs={'class': 'form-control'}),
            'seat': forms.Select(attrs={'class': 'form-control'}),
            'fuels': forms.Select(attrs={'class': 'form-control'}),
            'color_description': forms.TextInput(attrs={'class': 'form-control'}),
            'model_car': forms.TextInput(attrs={'class': 'form-control'}),
            'plate': forms.TextInput(attrs={'class': 'form-control'}),
            'chasis_number': forms.TextInput(attrs={'class': 'form-control'}),
            'vin_no': forms.TextInput(attrs={'class': 'form-control'}),
            'vehicle_type': forms.Select(attrs={'class': 'form-control'}),
            'rent_per_hr': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class DriverForm(ModelForm):
    class Meta:
        model = driver_shop
        fields = ['drivers_license','phone_number','drivers_rate']
        widgets = {
            'drivers_license': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'phone_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'drivers_rate': forms.NumberInput(attrs={'class': 'form-control'}),
}


class Rented_CarsForm(ModelForm):
    class Meta:
        model = Rented_Cars
        fields = ['renter_validid','driver_shp', 'pick_up_unit', 'return_unit']
        widgets = {
            'renter_validid': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'driver_shp': forms.Select(attrs={'class': 'form-control'}),
            'pick_up_unit': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'return_unit': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }
        input_formats = {
            'pick_up_unit': ['%Y-%m-%dT%H:%M'],  # Date and time format for 'datetime-local' input type
            'return_unit': ['%Y-%m-%dT%H:%M'],   # Date and time format for 'datetime-local' input type
        }

    def __init__(self, *args, **kwargs):
        super(Rented_CarsForm, self).__init__(*args, **kwargs)
        self.fields['driver_shp'].required = False  # Make driver_shp optional
