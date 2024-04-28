from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from . forms import *
from .models import *
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.template.defaulttags import register
from django.db.models import Avg
from django.db import connection

from django.db import connection

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

def home(request):
    return render(request, "home.html", {})

def login_veiw(request):
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
		return render(request, 'login.html', {})


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
                query = """
                    SELECT *
                    FROM app_apartmentbuilding
                    WHERE building_name = %s AND company_name = %s
                """
                with connection.cursor() as cursor:
                    cursor.execute(query,[building_name, company_name])
                    apartments = cursor.fetchall()
                # apartments = ApartmentBuilding.objects.filter(building_name = building_name).filter(company_name=company_name)
            elif  building_name and not company_name:
                query = """
                    SELECT *
                    FROM app_apartmentbuilding
                    WHERE building_name = %s
                """
                with connection.cursor() as cursor:
                    cursor.execute(query,[building_name])
                    apartments = cursor.fetchall()
                # apartments = ApartmentBuilding.objects.filter(building_name = building_name)
            elif  not building_name and company_name:
                query = """
                    SELECT *
                    FROM app_apartmentbuilding
                    WHERE company_name = %s
                """
                with connection.cursor() as cursor:
                    cursor.execute(query,[company_name])
                    apartments = cursor.fetchall()
                # apartments = ApartmentBuilding.objects.filter(company_name=company_name)
            else:
                query = """
                    SELECT *
                    FROM app_apartmentbuilding
                """
                with connection.cursor() as cursor:
                    cursor.execute(query)
                    apartments = cursor.fetchall()
                #  apartments = ApartmentBuilding.objects.all()
            return render(request, 'search_apartments.html', {'apartments':apartments, "form": form})
    else:
        form = ApartmentSearchForm()
        query = """
            SELECT *
            FROM app_apartmentbuilding
        """
        with connection.cursor() as cursor:
            cursor.execute(query)
            apartments = cursor.fetchall()
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
    query = """
        SELECT * FROM app_pet WHERE user_id = %s
    """
    with connection.cursor() as cursor:
        cursor.execute(query, [request.user])
        pets = cursor.fetchall()
    # print(pets)
    return render(request, 'pets.html', {"pets":pets})

def postInterest(request, pk):
    # apartment_unit = ApartmentUnit.objects.get(unit_rent_id = pk)
    if request.method == 'POST':
        form = InterestForm(request.POST, user=request.user, apartment_unit = pk)
        if form.is_valid():
            form.save()
            messages.success(request,"You have successfully posted your interest")
            return redirect('view_interest' , pk )
    else:
        form = InterestForm(user=request.user, apartment_unit = pk)
    return render(request, 'post_interests.html', {'form': form})

def viewInterests(request, pk):
    with connection.cursor() as cursor:
        # Execute raw SQL query
        cursor.execute("""
            SELECT * 
            FROM app_interests 
            WHERE username_id != %s 
            AND unit_rent_id_id = %s
        """, [request.user.username, pk])

        # Fetch all rows from the cursor
        rows = cursor.fetchall()
        print({"interests":rows})

    return render(request, 'interests.html', {"interests":rows, 'apartment_unit':pk})


def apartment(request, pk):
    allowed = []
    not_allowed = []
    flag = False
    # apartment = ApartmentBuilding.objects.get(id = pk)
    query = """
        SELECT * FROM app_apartmentbuilding WHERE id = %s
    """
    with connection.cursor() as cursor:
        cursor.execute(query, [pk])
        apartment = cursor.fetchone()
    query = """
        SELECT * FROM app_petpolicy WHERE apartment_building_id = %s AND is_allowed = %s
    """
    with connection.cursor() as cursor:
        cursor.execute(query, [pk, 1])
        pet_policy = cursor.fetchall()
    query = """
        SELECT * FROM app_pet WHERE user_id = %s
    """
    with connection.cursor() as cursor:
        cursor.execute(query, [request.user])
        pets = cursor.fetchall()
    query = """
        SELECT * FROM app_apartmentunit WHERE apartment_building_id = %s
    """
    with connection.cursor() as cursor:
        cursor.execute(query, [pk])
        apartment_units = cursor.fetchall()
    # pet_policy = PetPolicy.objects.filter(apartment_building_id = pk).filter(is_allowed = True)
    # pets = Pet.objects.filter(user = request.user)
    # apartment_units = ApartmentUnit.objects.filter(apartment_building = apartment)
    # rooms = Rooms.objects.filter(unit_rent_id__in = apartment_units)

    for pet in pets:
        flag = False
        for  policy in pet_policy:
            if policy[2] == pet[3] and policy[2] == pet[3]:
                allowed.append(pet)
                flag = True
                break
        if flag is not True:
            not_allowed.append(pet)
    print(allowed)
    return render(request, 'apartment.html', {'apartments':apartment, 'policies' : pet_policy, 'allowed':allowed, 'not_allowed': not_allowed, 'apartment_units':apartment_units}) 


def updatePet(request, pk):
    pet = Pet.objects.get(id = pk)
    form = PetForm(request.POST or None, user = request.user, instance = pet)
    if form.is_valid():
        form.save()
        messages.success(request,"You have successfully updated your pet")
        return redirect('viewPet')
    return render(request, 'update_pet.html', {"form":form})


def buildingUnitInfo(request):
    if request.method == 'POST':
        form = ApartmentUnitSearchForm(request.POST)
        if form.is_valid():
            building_name = form.cleaned_data['building_name']
            unit_number = form.cleaned_data['unit_number']
            if building_name and unit_number:
                # apartment = ApartmentBuilding.objects.get(building_name = building_name)
                # apartment_unit = ApartmentUnit.objects.filter(apartment_building = apartment).get(unit_number = unit_number)
                query = """
                    SELECT * FROM app_apartmentbuilding WHERE building_name = %s
                """
                with connection.cursor() as cursor:
                    cursor.execute(query, [building_name])
                    apartment = cursor.fetchone()
                if not apartment:
                    messages.success(request,"Does not exist!")
                    return render(request, 'search_unit.html', {"form": form})
                query = """
                    SELECT * FROM app_apartmentunit WHERE apartment_building_id = %s and unit_number = %s
                """
                with connection.cursor() as cursor:
                    cursor.execute(query, [apartment[0], unit_number])
                    apartment_unit = cursor.fetchone()
                if not apartment_unit:
                    messages.success(request,"Does not exist!")
                    return render(request, 'search_unit.html', {"form": form})
                query = """
                    SELECT * FROM app_rooms WHERE unit_rent_id_id = %s
                """
                with connection.cursor() as cursor:
                    cursor.execute(query, [apartment_unit[0]])
                    rooms = cursor.fetchall()
                bedrooms = 0; bathrooms = 0
                for  room in rooms:
                    if "bedroom" in room[1].lower():
                        bedrooms +=1
                    elif "bathroom" in room[1].lower():
                        bathrooms +=1            
                print(bedrooms, bathrooms)
                return render(request, 'search_unit.html', {'apartment':apartment, "unit":apartment_unit, "bedrooms": bedrooms, "bathrooms":bathrooms, "form": form})
            else:
                messages.success(request,"Give exact values!")
                return render(request, 'search_unit.html', {"form": form})

    else:
         form = ApartmentUnitSearchForm()
         return render(request, 'search_unit.html', {"form": form})
    

def advancedBuildingUnitInfo(request):
    if request.method == 'POST':
        form = AdvancedApartmentUnitSearchForm(request.POST)
        if form.is_valid():
            building_name = form.cleaned_data['building_name']
            expected_rent = form.cleaned_data['expected_rent']
            public_amenity_list = set(form.cleaned_data['public_amenities'])
            private_amenity_list = set(form.cleaned_data['private_amenities'])
            # apartment = ApartmentBuilding.objects.get(building_name = building_name)
            # apartment_unit = ApartmentUnit.objects.filter(apartment_building = apartment).filter(monthly_rent__gte = int(expected_rent)-100, monthly_rent__lte = int(expected_rent) + 100)
            query = """
                SELECT * FROM app_apartmentbuilding WHERE building_name = %s
            """
            with connection.cursor() as cursor:
                cursor.execute(query, [building_name])
                apartment = cursor.fetchone()
            if not apartment:
                messages.success(request,"Does not exist!")
                return render(request, 'advanced_search_unit.html', {"form": form})
            query = """
                SELECT *
                FROM app_apartmentunit
                WHERE apartment_building_id = %s
                AND monthly_rent >= %s
                AND monthly_rent <= %s
            """
            expected_rent_min = int(expected_rent) - 100
            expected_rent_max = int(expected_rent) + 100
            with connection.cursor() as cursor:
                cursor.execute(query, [apartment[0], expected_rent_min, expected_rent_max])
                apartment_unit = cursor.fetchall()
            if not apartment_unit:
                messages.success(request,"Does not exist!")
                return render(request, 'advanced_search_unit.html', {"form": form})
            bedrooms = {}; bathrooms = {}; filtered_apartment_units = []
            query = """
                SELECT atype_id
                FROM app_provides
                WHERE apartment_building_id = %s
            """
            with connection.cursor() as cursor:
                cursor.execute(query, [apartment[0]])
                building_amenities = cursor.fetchall()
            b_amenities = []
            for amenity in  building_amenities:
                b_amenities.append(amenity[0])
            # building_amenities = set([x.atype_id for x in Provides.objects.filter(apartment_building = apartment)])
            for apartment_unit_i in apartment_unit:
                query = """
                    SELECT atype_id
                    FROM app_amenitiesin
                    WHERE unit_rent_id_id = %s
                """
                with connection.cursor() as cursor:
                    cursor.execute(query, [apartment_unit_i[0]])
                    unit_amenities = cursor.fetchall()
                # unit_amenities = set([x.atype_id for x in AmenitiesIn.objects.filter(unit_rent_id = apartment_unit_i)])
                u_amenities = []
                for  amenity in unit_amenities:
                    u_amenities.append(amenity[0])

                if len(u_amenities) < len(private_amenity_list) or len(b_amenities) < len(public_amenity_list):
                    messages.success(request,"Try again!")  
                    return render(request, 'advanced_search_unit.html', {"form": form})

                if private_amenity_list.issubset(set(u_amenities)) and public_amenity_list.issubset(set(b_amenities)):    
                    filtered_apartment_units.append(apartment_unit_i)
                bed = 0; bath = 0
                query = """
                    SELECT * FROM app_rooms WHERE unit_rent_id_id = %s
                """
                with connection.cursor() as cursor:
                    cursor.execute(query, [apartment_unit_i[0]])
                    k = cursor.fetchall()
                # k = Rooms.objects.filter(unit_rent_id = apartment_unit_i)
                for  room in k:
                    if "bedroom" in room[1].lower():
                        bed +=1
                    elif "bathroom" in room[1].lower():
                        bath +=1
                bedrooms[apartment_unit_i] = bed
                bathrooms[apartment_unit_i] = bath
            if len(filtered_apartment_units) == 0:
               messages.success(request,"Try again!")  
            return render(request, 'advanced_search_unit.html', {'apartment':apartment, "unit":filtered_apartment_units, "form": form, "bedrooms":bedrooms, "bathrooms":bathrooms})
    else:
         form = AdvancedApartmentUnitSearchForm()
         return render(request, 'advanced_search_unit.html', {"form": form})
    

def searchInterest(request, pk):
    unit = ApartmentUnit.objects.get(pk=pk)
    if request.method == 'POST':
        form = SearchInterestForm(request.POST)
        if form.is_valid():
            roommates = form.cleaned_data['roommates']
            move_in_date_from = form.cleaned_data['move_in_date_from']
            move_in_date_to = form.cleaned_data['move_in_date_to']
            
            # Start building the raw SQL query
            query = "SELECT * FROM app_interests WHERE unit_rent_id_id = %s AND username_id != %s"
            params = [pk, request.user.username]
            
            if roommates:
                query += " AND roommate_cnt = %s"
                params.append(roommates)
            
            if move_in_date_from and move_in_date_to:
                query += " AND move_in_date >= %s AND move_in_date <= %s"
                params.extend([move_in_date_from, move_in_date_to])
            
            # Execute the raw SQL query
            with connection.cursor() as cursor:
                cursor.execute(query, params)
                interests = cursor.fetchall()
                
            return render(request, 'interests.html', {'interests': interests, 'apartment_unit': pk})
    else:
        form = SearchInterestForm()
    
    return render(request, 'search_Interest.html', {'form': form, 'unit': unit})

def zipcodeRentEstimate(request):
    if request.method == 'POST':
        form = ZipCodeSearchForm(request.POST)
        if form.is_valid():
            zipcode = form.cleaned_data['zipcode']
            try:
                buildings = ApartmentBuilding.objects.filter(addr_zipcode=zipcode)
                units = ApartmentUnit.objects.filter(apartment_building__in=buildings)
            except ApartmentBuilding.DoesNotExist:
                buildings = None
                units = None

            if units:
                units_with_rent = []
                allUnits = {}
                rent_sum = {}
                rent_count = {}
                for unit in units:
                    bedrooms = {}
                    bathrooms = {}
                    bed = 0
                    bath = 0
                    k = Rooms.objects.filter(unit_rent_id=unit)
                    for room in k:
                        if "bedroom" in room.name.lower():
                            bed += 1
                        elif "bathroom" in room.name.lower():
                            bath += 1
                    bedrooms[unit] = bed
                    bathrooms[unit] = bath
                    # units_with_rent.append({
                    #     'unit': unit,
                    #     'bedrooms': bed,
                    #     'bathrooms': bath,
                    # })
                    unitId = unit.unit_rent_id
                    allUnits[":bed:" +str(bedrooms[unit]) + ":bath:"+str(bathrooms[unit])] = {"bed" : bedrooms[unit], "bath" : bathrooms[unit]}
                    rent_sum[":bed:"+str(bedrooms[unit]) + ":bath:"+str(bathrooms[unit])] = rent_sum.get(":bed:"+str(bedrooms[unit]) + ":bath:"+str(bathrooms[unit]),0) + unit.monthly_rent
                    rent_count[":bed:"+str(bedrooms[unit]) + ":bath:"+str(bathrooms[unit])] = rent_count.get(":bed:"+str(bedrooms[unit]) + ":bath:"+str(bathrooms[unit]),0) + 1
                    
                avgRentUnit = {unitInfo : rent_sum[unitInfo]/rent_count[unitInfo] for unitInfo in rent_sum} 
                for unit in avgRentUnit:
                    units_with_rent.append({"bedroom": allUnits[unit]["bed"], "bathroom": allUnits[unit]["bath"], "avgRent": avgRentUnit[unit]})

                context = {
                    'zipcode': zipcode,
                    'units_with_rent': units_with_rent,
                    'form': form,
                    # 'avgRentUnit': avgRentUnit,
                    # 'bedrooms': bedrooms,
                    # 'bathrooms': bathrooms,
                }
                return render(request, 'estimateRent.html', context)
            else:
                context = {
                    'zipcode': zipcode,
                    'no_units_message': 'No available units satisfy the criteria in the given ZIP code.',
                    'form': form,
                }
                return render(request, 'estimateRent.html', context)
    else:
        form = ZipCodeSearchForm()
        return render(request, 'estimateRent.html', {'form': form})

def rentPriceView(request, pk):
    unit = ApartmentUnit.objects.get(unit_rent_id = pk)
    unit_rent = unit.monthly_rent
    unit_footage_upper = unit.square_footage  + (unit.square_footage * .1)
    unit_footage_lower = unit.square_footage  - (unit.square_footage * .1)
    building = unit.apartment_building
    city = building.addr_city
    buildings_in_city = ApartmentBuilding.objects.filter(addr_city=city)
    rent_sum = 0.0
    unit_count = 0.0
    for  bldg in buildings_in_city:
        unit_in_city = ApartmentUnit.objects.filter(apartment_building = bldg).filter(square_footage__gte = unit_footage_lower, square_footage__lte = unit_footage_upper).filter(~Q(unit_rent_id = pk))
        for u in unit_in_city:
            rent_sum += u.monthly_rent
            unit_count += 1
    if  unit_count > 0 :
        average_rent = rent_sum/unit_count
    else: 
        average_rent = 0
    data = [unit_rent, average_rent]

    return render(request, 'rent_price_view.html', {'data':data})	

