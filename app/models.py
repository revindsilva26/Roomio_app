from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Pet(models.Model):
    pet_name = models.CharField(max_length=50)
    pet_type = models.CharField(max_length=50)
    pet_size = models.CharField(max_length=20)
    user = models.ForeignKey(User, on_delete=models.CASCADE, to_field='username')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["pet_name","pet_type","user_id"], name="pet")
            ]

    def __str__(self):
        return f"{self.pet_name} ({self.pet_type})"
    

class ApartmentBuilding(models.Model):
    company_name = models.CharField(max_length=20)
    building_name = models.CharField(max_length=20)
    addr_num = models.IntegerField()
    addr_street = models.CharField(max_length=20)
    addr_city = models.CharField(max_length=20)
    addr_state = models.CharField(max_length=5)
    addr_zipcode = models.CharField(max_length=5)
    year_built = models.PositiveIntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["company_name","building_name"], name="apartment_building")
            ]

    def __str__(self):
        return f"{self.building_name} ({self.company_name})"
    

class ApartmentUnit(models.Model):
    unit_rent_id = models.AutoField(primary_key=True)
    unit_number = models.CharField(max_length=10)
    monthly_rent = models.IntegerField()
    square_footage = models.IntegerField()
    available_date_for_move_in = models.DateField()
    apartment_building = models.ForeignKey(ApartmentBuilding, on_delete=models.CASCADE)

    def __str__(self):
        return f"Unit {self.unit_number}"
    

class Rooms(models.Model):
    name = models.CharField(max_length=20)
    square_footage = models.IntegerField()
    description = models.CharField(max_length=50)
    unit_rent_id = models.ForeignKey(ApartmentUnit, on_delete=models.CASCADE, to_field='unit_rent_id')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["name","unit_rent_id"], name="room")
            ]

    def __str__(self):
        return f"{self.name} (Unit {self.unit_rent_id.unit_number})"


class PetPolicy(models.Model):
    pet_type = models.CharField(max_length=50)
    pet_size = models.CharField(max_length=20)
    is_allowed = models.BooleanField()
    registration_fee = models.IntegerField(null=True, blank=True)
    monthly_fee = models.IntegerField(null=True, blank=True)
    apartment_building = models.ForeignKey(ApartmentBuilding, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['pet_type', 'pet_size', 'apartment_building'], name='pet_policy')
        ]

    def __str__(self):
        return f"{self.pet_type} ({self.pet_size})"
    

class Amenities(models.Model):
    atype = models.CharField(max_length=20, primary_key=True)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.atype

class Interests(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE, to_field='username')
    unit_rent_id = models.ForeignKey(ApartmentUnit, on_delete=models.CASCADE, to_field='unit_rent_id')
    roommate_cnt = models.PositiveSmallIntegerField()
    move_in_date = models.DateField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['username','unit_rent_id'], name='interest')
        ]

    def __str__(self):
        return f"{self.username} - Unit {self.unit_rent_id}"
    
class AmenitiesIn(models.Model):
    atype = models.ForeignKey('Amenities', on_delete=models.CASCADE, to_field='atype')
    unit_rent_id = models.ForeignKey('ApartmentUnit', on_delete=models.CASCADE, to_field='unit_rent_id')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['atype','unit_rent_id'], name='amenities_in')
        ]

    def __str__(self):
        return f"{self.atype} - Unit {self.unit_rent_id}"
    

class Provides(models.Model):
    atype = models.ForeignKey('Amenities', on_delete=models.CASCADE, to_field='atype')
    company_name = models.CharField(max_length=20)
    building_name = models.CharField(max_length=20)
    fee = models.IntegerField()
    waiting_list = models.IntegerField()
    apartment_building = models.ForeignKey('ApartmentBuilding', on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['atype','apartment_building'], name='provide')
        ]

    def __str__(self):
        return f"{self.atype} for {self.apartment_building.building_name}, {self.apartment_building.company_name}"