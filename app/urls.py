
from django.urls import path
from  . import views

urlpatterns = [
    path("", views.home, name = "home"), # home page for the website
    path('login/', views.login_view, name='login'), 
    path("logout/", views.logout_user, name = "logout"), 
    path('register',views.register_user, name = "register"),
    path('search_apartment', views.searchApartment, name = 'search_apartment'),
    path('register_pet',views.registerPet, name = "register_pet"),
    path('pets',views.viewPet, name = "viewPet"),
    path('post_interests/<int:pk>',views.postInterest, name = "post_interest"),
    path('apartment/<int:pk>',views.apartment,name="apartment"),
    path('update_pet/<int:pk>',views.updatePet, name= "update_pet"),
    path('interests/<int:pk>',views.viewInterests, name = "view_interest"),
    path('search_building_unit', views.buildingUnitInfo, name = 'buildingUnitInfo'),
    path('advanced_search_building_unit', views.advancedBuildingUnitInfo, name = 'advancedBuildingUnitInfo'),
    path('searchInterest/<int:pk>', views.searchInterest, name= "searchInterest"),
    path('estimateRent', views.zipcodeRentEstimate, name= "estimateRent"),
    path('rentPriceView/<int:pk>', views.rentPriceView, name = "rentPriceView"),
]
