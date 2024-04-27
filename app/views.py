from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from . forms import *
from .models import *
from django.db.models import Q

def home(request):
	# Check to see if logging in
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		# Authenticate
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			messages.success(request, "You Have Been Logged In!")
			return redirect('home')
		else:
			messages.success(request, "There Was An Error Logging In, Please Try Again...")
			return redirect('home')
	else:
		return render(request, 'home.html', {})


def logout_user(request):
	logout(request)
	messages.success(request, "You Have Been Logged Out...")
	return redirect('home')

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username = username, password = password)
            login(request,user)
            messages.success(request,"You have successfully registered")
            return redirect('home')
    else:
        form = SignUpForm()
        return render(request, 'register.html',{'form': form})
    return render(request, 'register.html', {'form':form})


def searchApartment(request):
    if request.method == 'POST':
        form = ApartmentSearchForm(request.POST)
        if form.is_valid():
            building_name = form.cleaned_data['building_name']
            company_name = form.cleaned_data['company_name']
            apartments = []
            if building_name and company_name:
                apartments = ApartmentBuilding.objects.filter(building_name = building_name).filter(company_name=company_name)
            elif  building_name and not company_name:
                apartments = ApartmentBuilding.objects.filter(building_name = building_name)
            elif  not building_name and company_name:
                apartments = ApartmentBuilding.objects.filter(company_name=company_name)
            else:
                 apartments = ApartmentBuilding.objects.all()
            return render(request, 'search_apartments.html', {'apartments':apartments, "form": form})
    else:
         form = ApartmentSearchForm()
         apartments = ApartmentBuilding.objects.all()
         return render(request, 'search_apartments.html', {'apartments':apartments, "form": form})


def registerPet(request):
    if request.method == 'POST':
        form = PetForm(request.POST, user = request.user)
        if form.is_valid():
            form.save()
            messages.success(request,"You have successfully registered your pet")
            return redirect('viewPet')
    else:
        form = PetForm(user = request.user)
    return render(request, 'register_pet.html', {'form':form})	

def viewPet(request):
    pets = Pet.objects.filter(user = request.user)
    return render(request, 'pets.html', {'pets':pets})

def postInterest(request, pk):
    apartment_unit = ApartmentUnit.objects.get(unit_rent_id = pk)
    if request.method == 'POST':
        form = InterestForm(request.POST, user=request.user, apartment_unit = apartment_unit)
        if form.is_valid():
            form.save()
            messages.success(request,"You have successfully posted your interest")
            return redirect('view_interest' , pk )
    else:
        form = InterestForm(user=request.user, apartment_unit = apartment_unit)
    return render(request, 'post_interests.html', {'form': form})

def viewInterests(request, pk):
     interests = Interests.objects.filter(~Q(username = request.user)).filter(unit_rent_id_id = pk)
     return render(request, 'interests.html', {'interests':interests, 'apartment_unit':pk})


def apartment(request, pk):
    allowed = []
    not_allowed = []
    flag = False
    apartment = ApartmentBuilding.objects.get(id = pk)
    pet_policy = PetPolicy.objects.filter(apartment_building = apartment).filter(is_allowed = True)
    pets = Pet.objects.filter(user = request.user)
    apartment_units = ApartmentUnit.objects.filter(apartment_building = apartment)
    for pet in pets:
        flag = False
        for  policy in pet_policy:
              if policy.pet_size == pet.pet_size and policy.pet_type == pet.pet_type:
                   allowed.append(pet)
                   flag = True
                   break
        if flag is not True:
             not_allowed.append(pet)
        
    return render(request, 'apartment.html', {'apartments':apartment, 'policies' : pet_policy, 'allowed':allowed, 'not_allowed': not_allowed, 'apartment_units':apartment_units}) 


def updatePet(request, pk):
    pet = Pet.objects.get(id = pk)
    form = PetForm(request.POST or None, user = request.user, instance = pet)
    if form.is_valid():
        form.save()
        messages.success(request,"You have successfully updated your pet")
        return redirect('viewPet')
    return render(request, 'update_pet.html', {"form":form})