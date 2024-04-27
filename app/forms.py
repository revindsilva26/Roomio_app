from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import *


class DateInput(forms.DateInput):
    input_type = 'date'


class SignUpForm(UserCreationForm):
	email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}))
	first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}))
	last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}))


	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


	def __init__(self, *args, **kwargs):
		super(SignUpForm, self).__init__(*args, **kwargs)

		self.fields['username'].widget.attrs['class'] = 'form-control'
		self.fields['username'].widget.attrs['placeholder'] = 'User Name'
		self.fields['username'].label = ''
		self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

		self.fields['password1'].widget.attrs['class'] = 'form-control'
		self.fields['password1'].widget.attrs['placeholder'] = 'Password'
		self.fields['password1'].label = ''
		self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

		self.fields['password2'].widget.attrs['class'] = 'form-control'
		self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
		self.fields['password2'].label = ''
		self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'	
		

class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ('pet_name','pet_type','pet_size')
        widgets = {
			'pet_name': forms.TextInput(attrs = {'class':'form-control'}),
			'pet_type': forms.TextInput(attrs = {'class':'form-control'}),
			'pet_size': forms.TextInput(attrs = {'class':'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.user = self.user
        if commit:
            instance.save()
        return instance
		
class InterestForm(forms.ModelForm):
    class Meta:
        model = Interests
        fields = ('roommate_cnt', 'move_in_date')
        widgets = {
            'roommate_cnt': forms.NumberInput(attrs={'class': 'form-control'}),
            'move_in_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        apartment_unit = kwargs.pop('apartment_unit', None)
        super().__init__(*args, **kwargs)
        self.instance.username = user
        self.instance.unit_rent_id = apartment_unit

class ApartmentSearchForm(forms.Form):
    company_name = forms.CharField(max_length=20, required=False, label='Company Name')
    building_name = forms.CharField(max_length=20, required=False, label='Building Name')

    def clean(self):
        cleaned_data = super().clean()
        company_name = cleaned_data.get('company_name')
        building_name = cleaned_data.get('building_name')

        return cleaned_data

class ApartmentUnitSearchForm(forms.Form):
    building_name = forms.CharField(max_length=20, required=True, label='Building Name')
    unit_number = forms.CharField(max_length=5, required=False, label='Unit Number')
    def clean(self):
        cleaned_data = super().clean()
        unit_number = cleaned_data.get('unit_number')
        building_name = cleaned_data.get('building_name')
        return cleaned_data
    
class AdvancedApartmentUnitSearchForm(forms.Form):
    public_amenities_list = set([(amenity.atype, amenity.atype) for amenity in list(Provides.objects.all())])
    private_amenities_list = set([(amenity.atype, amenity.atype) for amenity in list(AmenitiesIn.objects.all())])
    building_name = forms.CharField(max_length=20, required=True, label='Building Name')
    expected_rent = forms.DecimalField(max_digits=20, required = False, label = 'Expected Rent')
    public_amenities = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=public_amenities_list, required=False, label='Public Amenities')
    private_amenities = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=private_amenities_list, required= False, label = 'Private Amenities')
    def clean(self):
        cleaned_data = super().clean()
        building_name = cleaned_data.get('building_name')
        expected_rent = cleaned_data.get('expected_rent')
        public_amenities = cleaned_data.get('public_amenities')
        private_amenities = cleaned_data.get('private_amenities')
        return cleaned_data
    

class SearchInterestForm(forms.Form):
    roommates = forms.DecimalField(max_digits=20, required=False, label='Roommates')
    move_in_date_from = forms.DateField(widget= DateInput, required= False, label="Move-In Date From")
    move_in_date_to = forms.DateField(widget=DateInput, required= False, label="Move-In Date To")
    def clean(self):
        cleaned_data = super().clean()
        roommates = cleaned_data.get('roommates')
        move_in_date_from = cleaned_data.get('move_in_date_from')
        move_in_date_to = cleaned_data.get('move_in_date_to')
        return cleaned_data