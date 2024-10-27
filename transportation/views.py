
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from transportation.decorators import role_required
from django.core.paginator import Paginator
from .forms import *
from datetime import datetime
from django.utils.timezone import now 



Brands = (
    ('toyota', 'Toyota'),
    ('honda', 'Honda'),
    ('mitsubishi', 'Mitsubishi'),
    ('chevrolet', 'Chevrolet'),
    ('ford', 'Ford'),
    ('nissan', 'Nissan'),
    ('bmw', 'BMW'),
    ('mercedes_benz', 'Mercedes-Benz'),
    ('audi', 'Audi'),
    ('volkswagen', 'Volkswagen'),
    ('hyundai', 'Hyundai'),
    ('kia', 'Kia'),
    ('tesla', 'Tesla'),
    ('subaru', 'Subaru'),
    ('mazda', 'Mazda'),
    ('volvo', 'Volvo'),
    ('lexus', 'Lexus'),
    ('porsche', 'Porsche'),
    ('ferrari', 'Ferrari'),
    ('lamborghini', 'Lamborghini'),
    ('land_rover', 'Land Rover'),
    ('jaguar', 'Jaguar'),
    ('infiniti', 'Infiniti'),
    ('acura', 'Acura'),
    ('jeep', 'Jeep'),
    ('dodge', 'Dodge'),
    ('ram', 'Ram'),
    ('chrysler', 'Chrysler'),
    ('buick', 'Buick'),
    ('gmc', 'GMC'),
    ('cadillac', 'Cadillac'),
    ('peugeot', 'Peugeot'),
    ('renault', 'Renault'),
    ('citroen', 'Citroën'),
    ('fiat', 'Fiat'),
    ('alfa_romeo', 'Alfa Romeo'),
    ('suzuki', 'Suzuki'),
    ('skoda', 'Škoda'),
    ('seat', 'SEAT'),
    ('bentley', 'Bentley'),
    ('rolls_royce', 'Rolls-Royce'),
    ('aston_martin', 'Aston Martin'),
    ('maserati', 'Maserati'),
    ('lotus', 'Lotus'),
    ('mclaren', 'McLaren'),
    ('bugatti', 'Bugatti'),
    ('saab', 'Saab'),
    ('opel', 'Opel'),
)


transmission = (
    ('manual', 'Manual'),
    ('automatic', 'Automatic'),
    ('semi', 'Semi-Automatic'),
    ('cvt', 'Continuously Variable Transmission (CVT)'),
    ('dual_clutch', 'Dual-Clutch Transmission (DCT)'),
    ('tiptronic', 'Tiptronic'),
    ('electric', 'Electric'),
)


seat = (
    (2, '2 Seater'),
    (4, '4 Seater'),
    (5, '5 Seater'),
    (6, '6 Seater'),
    (7, '7 Seater'),
    (8, '8 Seater'),
    (9, '9 Seater'),
    (10, '10 Seater'),
)



fuel_types = (
    ('diesel', 'Diesel'),
    ('gasoline', 'Gasoline'),
    ('electric', 'Electric'),
    ('hybrid', 'Hybrid'),
    ('plug_in_hybrid', 'Plug-in Hybrid'),
    ('cng', 'Compressed Natural Gas (CNG)'),
    ('lpg', 'Liquefied Petroleum Gas (LPG)'),
    ('hydrogen', 'Hydrogen'),
    ('ethanol', 'Ethanol'),
    ('biodiesel', 'Biodiesel'),
    ('synthetic', 'Synthetic Fuel (eFuel)'),
)

vehicle_type = (
    ('sedan', 'Sedan'),
    ('suv', 'SUV (Sport Utility Vehicle)'),
    ('hatchback', 'Hatchback'),
    ('coupe', 'Coupe'),
    ('convertible', 'Convertible'),
    ('wagon', 'Wagon'),
    ('pickup', 'Pickup Truck'),
    ('van', 'Van'),
    ('motorcycle', 'Motorcycle'),
    ('bus', 'Bus'),
    ('truck', 'Truck'),
    ('minivan', 'Minivan'),
    ('crossover', 'Crossover'),
    ('electric', 'Electric Vehicle'),
    ('hybrid', 'Hybrid Vehicle'),
    ('sports', 'Sports Car'),
)



def home(request):
    controlsite = get_object_or_404(controls, pk=1)
    if controlsite.control == 1:
        return redirect(controlsite.site)
    
    context = {
    }
    return render(request,'public/index.html',context)

def vehicle(request):
    vehicle = Vehicle.objects.filter(status="published")
    context = {
        "vehicle":vehicle,
    }
    return render(request,'public/vehicle.html',context)

def drivers(request):
    context = {
    }
    return render(request,'public/drivers.html',context)

def car_details(request, pk):
    vehicle_details = get_object_or_404(Vehicle,pk=pk)
    shop = vehicle_details.shop_belong.id
    shop_details = get_object_or_404(Shops,pk=shop)
    
    context = {
        "vehicle_details":vehicle_details,
        "shop_details":shop_details,
    }
    return render(request,'public/car_details.html',context)

def driver_details(request):
    context = {
    }
    return render(request,'public/driver_details.html',context)


def shop(request):
    context = {
        
    }
    return render(request,'public/shop.html',context)

def shop_details(request):
    context = {
        
    }
    return render(request,'public/shop_details.html',context)


def contacts(request):
    context = {
        
    }
    return render(request,'public/contact.html',context)


def createaacount(request):
    
    form = MyUserCreationForm()
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            request.session['unverified_email'] =  user.email
            user.username = user.username.lower()
            user.code = int(get_random_string(length=6, allowed_chars='1234567890'))
            user.save()
            # Send OTP to the user's email
            subject = 'Your OTP for Registration'
            message = f'Your OTP is {user.code}. Enter this code to complete your registration.'
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = user.email
            send_mail(subject, message, from_email, [to_email], fail_silently=False)

            # login(request, user, backend='django.contrib.auth.backends.ModelBackend')  # for Direct log in after registration
            messages.success(request, 'Account Created Successfully')
            return redirect('verify_email')
        else:
            messages.error(request, 'An error occurred during registration')
    
    context = {
        'form': form,
    }
    return render(request,'public/createaacount.html',context)



def verify_email(request):
    if request.method == 'POST':
        otp = request.POST.get("otp")
        email = request.session['unverified_email']

        if not email:
            messages.error(request, 'Email not found in session')
            return redirect('signin')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'User not found')
            return redirect('signin')

        # Perform pattern match on user code
        if str(user.code) == otp:
            user.status = "verified"
            user.code = 0  # Assuming 0 represents the verified status
            user.save()
            # messages.info(request, 'Account verified and signed in successfully...')
            # subject = 'Account Verification'
            # message = f'Congratulations! Your account is now verified. You can now log in. '
            # from_email = settings.DEFAULT_FROM_EMAIL
            # to_email = user.email
            # send_mail(subject, message, from_email, [to_email], fail_silently=False)
            # request.session.flush()
            messages.success(request, "Account Verified")
            return redirect('home')
        else:
            messages.error(request, "Code doesn't match")

    return render(request, 'public/verify.html')



def signin(request):
    page = 'login'
    if request.user.is_authenticated:
        
        return redirect('admin')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'Account does not exist')
            return render(request, 'public/signin.html', {'page': page})

        user = authenticate(request, email=email, password=password)

        if user is not None:
            # Check user's status and code
            if user.status == 'verified' or user.code == 0:
                if user.lock == 'restricted':
                    logout(request)
                    messages.error(request,'Please Try Again Later.')
                    return redirect('signin')
                else:
                    user.log_status = "online"
                    user.save()
                    login(request, user)
                    messages.success(request,'Login succesfully')
                    return redirect('admin')
            else:
                # Save email in session and render a template for email verification
                request.session['unverified_email'] = email
                messages.success(request,'Please Verify your Account')
                return render(request, 'public/verify.html', {'user': user})
        else:
            messages.error(request, 'Username OR password does not exist')

    context = {
        'page': page,
        }
    return render(request,'public/signin.html')


#============================================================================================================
#ADMINISTRATORS


@login_required(login_url='signin')
@role_required(allowed_roles=['1'], redirect_url='users')
def admin(request):
    page = 'homedashboard'
    title_page = 'administrator'
    users = request.user
    context = {
        'page':page,
        'title_page':title_page,
        'users':users,
       
    }
    return render(request, 'accounts/index.html',context)


@login_required(login_url='signin')
@role_required(allowed_roles=['1'], redirect_url='users')
def blank(request):
    page = 'blank'
    title_page = 'blank'
    users = request.user
    context = {
        'page':page,
        'title_page':title_page,
        'users':users,
       
    }
    return render(request, 'accounts/blank.html',context)


@login_required(login_url='signin')
@role_required(allowed_roles=['1'], redirect_url='users')
def list_administrators(request):
    page = 'adminlist'
    title_page = 'Administrator list'
    users = request.user
    admins = User.objects.filter(roles='1')
    form = MyUserCreationForm()
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            add_admin = form.save(commit=False)
            raw_password = form.cleaned_data.get('password1')
            request.session['unverified_email'] =  add_admin.email
            add_admin.username = add_admin.username.lower()
            add_admin.roles = '1'
            add_admin.code = int(get_random_string(length=6, allowed_chars='1234567890'))
            add_admin.save()
            # Send OTP to the user's email
            subject = 'Access Administrative Accounts'
            message = f'''
                        Hi admin, this is ypur administrative credentials
                        Account Email :{add_admin.email} ,
                        Password: {raw_password} ,
                        Your OTP is {add_admin.code}. Enter this code to complete your autherntications.'''
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = add_admin.email
            send_mail(subject, message, from_email, [to_email], fail_silently=False)

            # login(request, user, backend='django.contrib.auth.backends.ModelBackend')  # for Direct log in after registration
            messages.success(request, 'Account Created Successfully')
            return redirect('list_administrators')
        else:
            messages.error(request, 'An error occurred during registration')
    context = {
        'page':page,
        'title_page':title_page,
        'users':users,
        'form': form,
        'admins':admins,
       
    }
    return render(request, 'accounts/administrators.html',context)


@login_required(login_url='signin')
@role_required(allowed_roles=['1','2'], redirect_url='logoutUser')
def profile(request):
    users = request.user
    current_email = users.email
    user_id = users.id
    my_shops = Shops.objects.filter(owner=users)
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=users )
        if form.is_valid():
            form.save()
            messages.success(request, "Saved Successfully")
            return redirect('profile')
        else:
             messages.error(request, "Please Try Again")
    else:
        form = UserForm(instance=users)
    context = {
        'current_email':current_email,
        'form':form,
        'users':users,
        'my_shops':my_shops,
    }
    return render(request, 'accounts/profile.html',context)


@login_required(login_url='signin')
@role_required(allowed_roles=['1'], redirect_url='users')
def shops(request):
    users = request.user
    page = 'regshops'
    title_page = 'Registered Shops'


    list_shops = Shops.objects.all()
    
    context = {
        'page':page,
        'title_page':title_page,
        'users':users,
        'list_shops':list_shops,

    }
    return render(request,'accounts/shops.html',context)


@login_required(login_url='signin')
@role_required(allowed_roles=['1'], redirect_url='users')
def vehicles_list(request):
    users = request.user
    page = 'regcars'
    title_page = 'Registered Cars'


    list_vehicles = Vehicle.objects.all()
    
    context = {
        'page':page,
        'title_page':title_page,
        'users':users,
        'list_vehicles':list_vehicles,

    }
    return render(request,'accounts/vehicles_list.html',context)



@login_required(login_url='signin')
@role_required(allowed_roles=['1'], redirect_url='users')
def unlock_shops(request, pk):
    shop_details = get_object_or_404(Shops, pk=pk)
    if shop_details.status == 'lock':
        shop_details.status = 'published'
        shop_details.save()
        messages.success(request, "Shop published")
    else:
        shop_details.status = 'lock'
        shop_details.save()
        messages.success(request, "Shop set to lock")
    return redirect('shops')

@login_required(login_url='signin')
@role_required(allowed_roles=['1'], redirect_url='users')
def published_cars(request, pk):
    car_details = get_object_or_404(Vehicle, pk=pk)
    if car_details.status == 'uncheck':
        car_details.status = 'published'
        car_details.save()
        messages.success(request, "Car registration approved")
    else:
        car_details.status = 'uncheck'
        car_details.save()
        messages.success(request, "Car registration disapprove")
    return redirect('vehicles_list')
#============================================================================================================


@login_required(login_url='signin')
@role_required(allowed_roles=['2'], redirect_url='admin')
def users(request):
    users = request.user
    page = 'homedashboard'
    title_page = 'Prime Cars'
    
    my_shops = Shops.objects.filter(owner=users)
    registred_shops = Shops.objects.filter(status="published")[:12]
    rented_cars = Rented_Cars.objects.filter(renters=users)

    context = {
        'page':page,
        'title_page':title_page,
        'users':users,
        'my_shops':my_shops, 
        'registred_shops':registred_shops,
        'rented_cars':rented_cars,
    }
    return render(request, 'accounts/index_users.html',context)

@login_required(login_url='signin')
@role_required(allowed_roles=['2'], redirect_url='admin')
def myshops(request):
    users = request.user
    page = 'myshops'
    title_page = 'My Shops'
    my_shops = Shops.objects.filter(owner=users)
    
    if request.method == 'POST':
        form = ShopForm(request.POST, request.FILES)
        if form.is_valid():
            shop = form.save(commit=False)  # Don't save to the database yet
            shop.owner = users  # Set the owner to the logged-in user
            shop.save()  # Now save to the database
            messages.success(request, "Saved Successfully")
            return redirect('myshops')
        else:
            print(form.errors)  # Print form errors to debug
            messages.error(request, "Please Try Again")
    else:
        form = ShopForm()

    context = {
        'page': page,
        'title_page': title_page,
        'users': users,
        'form': form,
        'my_shops': my_shops,
    }
    return render(request, 'accounts/myshops.html', context)




@login_required(login_url='signin')
@role_required(allowed_roles=['2'], redirect_url='admin')
def edit_myshops(request,slug):
    users = request.user
    page = 'myslistshop'
    title_page = 'Edit Shop details'
    my_shops = Shops.objects.filter(owner=users)
    shop_instance = get_object_or_404(Shops,slug=slug)
    if request.method == 'POST':
        form = ShopForm(request.POST, request.FILES,instance=shop_instance)
        if form.is_valid():
            shop = form.save(commit=False) # Don't save to the database yet
            shop.status = 'lock'
            new_slug = slugify(shop.shop_name)
            shop.slug = new_slug
            shop.owner = users  # Set the owner to the logged-in user
            shop.save()  # Now save to the database
            messages.success(request, "Saved Successfully")
            return redirect('mylistshop')
        else:
            messages.error(request, "Please Try Again")
    else:
        form = ShopForm(instance=shop_instance)

    context = {
        'page': page,
        'title_page': title_page,
        'users': users,
        'form': form,
        'my_shops':my_shops,
        'shop_instance':shop_instance,
    }
    return render(request, 'accounts/myshops.html', context)


@login_required(login_url='signin')
@role_required(allowed_roles=['2'], redirect_url='admin')
def delete_myshops(request, slug):
    shop_del = get_object_or_404(Shops, slug=slug)
    shop_del.delete()
    messages.success(request, "Shop Deleted successfully")
    return redirect('mylistshop')

@login_required(login_url='signin')
@role_required(allowed_roles=['2'], redirect_url='admin')
def mylistshop(request):
    users = request.user
    page = 'myslistshop'
    title_page = 'My Shops'
    my_shops = Shops.objects.filter(owner=users)

    context = {
        'page':page,
        'title_page':title_page,
        'users':users,
        'my_shops':my_shops, 
    }
    return render(request, 'accounts/mylistshop.html',context)


@login_required(login_url='signin')
@role_required(allowed_roles=['2'], redirect_url='admin')
def registered_shops(request):
    users = request.user
    page = 'regshops'
    title_page = 'Registered Shops'
    my_shops = Shops.objects.filter(owner=users)
    registred_shops = Shops.objects.filter(status="published")

    context = {
        'page':page,
        'title_page':title_page,
        'users':users,
        'my_shops':my_shops, 
        'registred_shops':registred_shops,
    }
    return render(request, 'accounts/registered_shops.html',context)


@login_required(login_url='signin')
@role_required(allowed_roles=['2'], redirect_url='admin')
def details_shops(request,slug):
    users = request.user
    details_shop = get_object_or_404(Shops,slug=slug)
    shopname = details_shop.shop_name
    page = 'regshops'
    title_page = shopname


    my_shops = Shops.objects.filter(owner=users)
    registred_shops = Shops.objects.filter(status="published")
    approve_driver = driver_shop.objects.filter(shop_under=details_shop,status=1)
    driver_aplication = driver_shop.objects.filter(account=users)
    droptyple = Vehicle.objects.all()
    if request.method=="POST":
        searchbrand= request.POST.get('brand')
        searchfuel = request.POST.get('fuel')
        searchseat = request.POST.get('seat')
        searchtransmission= request.POST.get('transmission')
        vehicles = Vehicle.objects.filter(shop_belong=details_shop,categories=searchbrand,fuels=searchfuel,seat=searchseat,transmission=searchtransmission)
    else:
        vehicles = Vehicle.objects.filter(shop_belong=details_shop)

    paginator = Paginator(vehicles, 3)  
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    paginator_approve_driver = Paginator(approve_driver, 8)  
    page_number_driver = request.GET.get("drivers")
    page_obj_driver = paginator_approve_driver.get_page(page_number_driver)
    context = {
        'page':page,
        'title_page':title_page,
        'users':users,
        'my_shops':my_shops, 
        'registred_shops':registred_shops,
        'details_shop':details_shop,
        'vehicles':vehicles,
        'droptyple':droptyple,
        'page_obj':page_obj,
        'slug':slug,
        'page_obj_driver':page_obj_driver,
        'Brands':Brands,
        'fuel_types':fuel_types,
        'seat':seat,
        'transmission':transmission,
        'driver_aplication':driver_aplication,
        
    }
    return render(request, 'accounts/detail_registered_shops.html',context)


@login_required(login_url='signin')
@role_required(allowed_roles=['2'], redirect_url='admin')
def myshop_details(request,slug):
    users = request.user
    page = 'myslistshop'
    title_page = 'Shop Details'
    my_shops = Shops.objects.filter(owner=users)
    shops = get_object_or_404(Shops,slug=slug)
    count_vehicles = Vehicle.objects.filter(shop_belong=shops).count()
    count_not_approve = driver_shop.objects.filter(shop_under=shops ,status=0).count()
    drivers_list = driver_shop.objects.filter(shop_under=shops,status=1)
    count_approve = driver_shop.objects.filter(shop_under=shops,status=1).count()
    rented_cars = Rented_Cars.objects.filter(unit_rented__shop_belong__in=my_shops)
    context = {
        'page':page,
        'title_page':title_page,
        'users':users,
        'my_shops':my_shops,
        'shops':shops,
        'count_vehicles':count_vehicles,
        'count_not_approve':count_not_approve,
        'drivers_list':drivers_list,
        'count_approve':count_approve,
        'rented_cars':rented_cars
    }
    return render(request,'accounts/myshop_details.html',context)





@login_required(login_url='signin')
@role_required(allowed_roles=['2'], redirect_url='admin')
def vehicles(request, slug):
    users = request.user
    page = 'myslistshop'
    title_page = 'Vehicles'
    my_shops = Shops.objects.filter(owner=users)
    shops = get_object_or_404(Shops, slug=slug)
    shopID = shops.id
    garage = Vehicle.objects.filter(shop_belong=shopID)
    
    if request.method == 'POST':
        form = VehicleForm(request.POST, request.FILES)
        if form.is_valid():
            ve = form.save(commit=False)  # Don't save to the database yet
            ve.shop_belong = shops
            ve.save()  # Now save to the database
            messages.success(request, "Saved Successfully")
            return redirect('vehicles',slug)
        else:
            print(form.errors)  # Debug form errors
            messages.error(request, "Please Try Again")
    else:
        form = VehicleForm()

    context = {
        'page': page,
        'title_page': title_page,
        'users': users,
        'my_shops': my_shops,
        'shops': shops,
        'form': form,
        'slug':slug,
        'garage':garage
    }
    return render(request, 'accounts/vehicles.html', context)



@login_required(login_url='signin')
@role_required(allowed_roles=['2'], redirect_url='admin')
def shopdrivers(request, slug):
    users = request.user
    page = 'regshops'
    title_page = 'Driver Registration '
    my_shops = Shops.objects.filter(owner=users)
    shops = get_object_or_404(Shops, slug=slug)
    shopID = shops.id
    garage = Vehicle.objects.filter(shop_belong=shopID)
    check_driver = driver_shop.objects.filter(shop_under=shops,account=users)
   

    if request.method == 'POST':
        form = DriverForm(request.POST, request.FILES)
        if form.is_valid():
            driver = form.save(commit=False)  # Don't save to the database yet
            driver.account = users
            driver.shop_under = shops
            driver.save()  # Now save to the database
            messages.success(request, "Saved Successfully")
            return redirect('shopdrivers',slug)
        else:
            print(form.errors)  # Debug form errors
            messages.error(request, "Please Try Again")
    else:
        form = DriverForm()

    context = {
        'page': page,
        'title_page': title_page,
        'users': users,
        'my_shops': my_shops,
        'shops': shops,
        'form': form,
        'slug':slug,
        'garage':garage,
        'check_driver':check_driver,
        
    }
    return render(request, 'accounts/shopdrivers.html', context)


@login_required(login_url='signin')
@role_required(allowed_roles=['2'], redirect_url='admin')
def edit_vehicles(request, slug, pk):
    users = request.user
    page = 'myslistshop'
    title_page = 'Vehicles'
    my_shops = Shops.objects.filter(owner=users)
    shops = get_object_or_404(Shops, slug=slug)
    shopID = shops.id
    garage = Vehicle.objects.filter(shop_belong=shopID)
    vehicle = get_object_or_404(Vehicle, pk=pk, shop_belong=shops) 
    
    if request.method == 'POST':
        form = VehicleForm(request.POST, request.FILES, instance=vehicle)
        if form.is_valid():
            ve = form.save(commit=False) 
            ve.shop_belong = shops
            ve.status = "uncheck"  # Assign the Shops object itself
            ve.save()  
            messages.success(request, "Vehicle updated successfully")
            return redirect('vehicles', slug=slug)  
        else:
            print(form.errors)  # For debugging form errors
            messages.error(request, "Please try again")
    else:
        form = VehicleForm(instance=vehicle)

    context = {
        'page': page,
        'title_page': title_page,
        'users': users,
        'my_shops': my_shops,
        'shops': shops,
        'form': form,
        'slug':slug,
        'garage': garage,
    }

    return render(request, 'accounts/vehicles.html', context)


@login_required(login_url='signin')
@role_required(allowed_roles=['2'], redirect_url='admin')
def mydrivers(request, slug):
    users = request.user
    page = 'myslistshop'
    title_page = 'My Drivers'
    my_shops = Shops.objects.filter(owner=users)
    shops = get_object_or_404(Shops, slug=slug)
    shopID = shops.id
    garage = Vehicle.objects.filter(shop_belong=shopID)
    aply_drivers = driver_shop.objects.filter(shop_under=shops,status=0)
    reg_drivers = driver_shop.objects.filter(shop_under=shops, status__in=[1, 2])
    check_driver = driver_shop.objects.filter(shop_under=shops,account=users)
    context = {
        'page': page,
        'title_page': title_page,
        'my_shops':my_shops,
        'aply_drivers':aply_drivers,
        'reg_drivers':reg_drivers,
        'slug':slug,
        'users':users
    }
    return render(request, 'accounts/drivers.html', context)

@login_required(login_url='signin')
@role_required(allowed_roles=['2'], redirect_url='admin')
def approved_driver(request, slug, pk):
    shop_details = get_object_or_404(Shops, slug=slug) 
    driver_approved = get_object_or_404(driver_shop, pk=pk)
    email = driver_approved.account.email
    shop_name = shop_details.shop_name
    address = shop_details.address
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = email
    
    
    if driver_approved.status == 1:
        subject = 'Driver Status Updated'
        message = f'''
            Good Day to our skillfull driver of our shop {shop_name}, we are notifying you that your account is temporarily 
            dismmised, please visit to our office at {address} for further information.'''
        driver_approved.status = 2
        messages.success(request, "Driver Status Temporary dismissed")
    elif driver_approved.status == 2:
        subject = 'Driver Registration Re-Approved'
        message = f'''
            Congratulations your status as driver in our shop "{shop_name}" is re-deployed.
            please visit to our office at {address} for further information.'''
        driver_approved.status = 1
        messages.success(request, "Driver Status Re-deployed")
    else:
        subject = 'Driver Registration Approved'
        message = f'''
            Congratulations your registration as driver in our shop "{shop_name}" is approved.
            please visit to our office at {address} for further information.'''
        driver_approved.status = 1
        messages.success(request, "Driver Registration Approved")

    send_mail(subject, message, from_email, [to_email], fail_silently=False)
    driver_approved.save()  
    return redirect('mydrivers', slug=slug)


@login_required(login_url='signin')
@role_required(allowed_roles=['2'], redirect_url='admin')
def delete_driver(request, slug, pk):
    driver_delete = get_object_or_404(driver_shop, pk=pk)
    shop_details = get_object_or_404(Shops, slug=slug) 
    email = driver_delete.account.email
    shop_name = shop_details.shop_name
    address = shop_details.address
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = email
    subject = 'Driver Registration Denied'
    message = f'''
            Hi to our aspring driver to this shop "{shop_name}", we are humbly to say that, 
            we disapproved your driver aplications, due to some reason like,
            1, data are not match in drivers licence.
            2, unrealistic input in application.

            please visit to our office at {address} for further information.'''
    send_mail(subject, message, from_email, [to_email], fail_silently=False)
    messages.success(request, "Driver Denied")
    driver_delete.delete() 
    return redirect('mydrivers', slug=slug)



@login_required(login_url='signin')
@role_required(allowed_roles=['2'], redirect_url='admin')
def delete_vehicles(request, slug, pk):
    vehicle_delete = get_object_or_404(Vehicle, pk=pk) 
    vehicle_delete.delete()  
    messages.success(request, "Vehicle deleted successfully")
    return redirect('vehicles', slug=slug) 









@login_required(login_url='signin')
@role_required(allowed_roles=['2'], redirect_url='admin')
def shop_unit(request, slug , pk):
    users = request.user
    cars = get_object_or_404(Vehicle, pk=pk)
    cars_name = cars.categories
    page = 'regshops'
    title_page = cars_name
    my_shops = Shops.objects.filter(owner=users)
    details_shop = get_object_or_404(Shops,slug=slug)
    context = {
        'page':page,
        'title_page':title_page,
        'users':users,
        'my_shops':my_shops, 
        'details_shop':details_shop,
        'slug':slug,
        'cars':cars
    }
    return render(request, 'accounts/shopunit.html',context)


@login_required(login_url='signin')
@role_required(allowed_roles=['2'], redirect_url='admin')
def registered_vehicles(request):
    users = request.user
    page = 'regcars'
    title_page = 'Registered Cars'
    my_shops = Shops.objects.filter(owner=users)
    if request.method=="POST":
        searchbrand= request.POST.get('brand')
        searchfuel = request.POST.get('fuel')
        searchseat = request.POST.get('seat')
        searchtransmission= request.POST.get('transmission')
        vehicles = Vehicle.objects.filter(categories=searchbrand,fuels=searchfuel,seat=searchseat,transmission=searchtransmission).exclude(status="uncheck")
    else:
        vehicles = Vehicle.objects.exclude(status="uncheck")

    paginator = Paginator(vehicles, 3)  
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        'page':page,
        'title_page':title_page,
        'users':users,
        'my_shops':my_shops,
        'page_obj':page_obj,
        'Brands':Brands,
        'fuel_types':fuel_types,
        'seat':seat,
        'transmission':transmission,
    }
    return render(request, 'accounts/registered_vehicles.html',context)

@login_required(login_url='signin')
@role_required(allowed_roles=['2'], redirect_url='admin')
def rent_vehicles(request, pk):
    users = request.user
    cars = get_object_or_404(Vehicle, pk=pk)
    unit = pk
    check_spamming = Rented_Cars.objects.filter(renters=users,unit_rented=cars).count()
    current_time = now()
    if check_spamming > 0:
        messages.error(request, "You rented that car already")
        return redirect('registered_vehicles')
        
    else:
        car_hourly_rate  = cars.rent_per_hr
        carshop = cars.shop_belong.id
        shop_detail = get_object_or_404(Shops, pk=carshop)
        car_name = cars.categories
        my_shops = Shops.objects.filter(owner=users)
        page = 'regcars'
        title_page = "Rent " + car_name
        
        if request.method == 'POST':
            form = Rented_CarsForm(request.POST, request.FILES)
            if form.is_valid():
                rented = form.save(commit=False)  
                rented.renters = users
                rented.unit_rented = cars
                
                driver_id = request.POST.get('driver_shp')
                if driver_id: 
                    driver_details = driver_shop.objects.get(id=driver_id)
                    hourly_rate = driver_details.drivers_rate
                    rented.driver_shp = driver_details
                else:
                    hourly_rate = 0
                if rented.pick_up_unit > current_time :
                    if rented.return_unit > rented.pick_up_unit:
                        duration = rented.return_unit - rented.pick_up_unit
                    else:
                        messages.error(request, "Set time Correctly,please try again")
                        return redirect('rent_vehicles', pk=pk)
                else:
                    messages.error(request, "Set time Correctly,please try again")
                    return redirect('rent_vehicles', pk=pk)

                total_hours = duration.total_seconds() / 3600

                combine_rate = hourly_rate + car_hourly_rate

                total_cost = combine_rate * total_hours
                rented.total_hrs = total_hours 
                rented.total_fare = total_cost
                rented.save() 
                messages.success(request, "Successfully Transactions")
                return redirect('users')
            else:
                messages.error(request, "Please try again.")
        else:
            form = Rented_CarsForm()
    
    context = {
        'page': page,
        'title_page': title_page,
        'my_shops': my_shops,
        'shop_detail': shop_detail,
        'car_name': car_name,
        'cars': cars,
        'form': form,
        'current_time':current_time,
        'users':users,
        'unit':unit

    }
    
    return render(request, 'accounts/rent_cars.html', context)





@login_required(login_url='signin')
@role_required(allowed_roles=['2'], redirect_url='admin')
def rent_vehicles_edit(request, unit, renteid):
    users = request.user
    cars = get_object_or_404(Vehicle, pk=unit)
    rentdetails = get_object_or_404(Rented_Cars, pk=renteid)
    current_time = now()
    
    car_hourly_rate  = cars.rent_per_hr
    carshop = cars.shop_belong.id
    shop_detail = get_object_or_404(Shops, pk=carshop)
    car_name = cars.categories
    my_shops = Shops.objects.filter(owner=users)
    page = 'regcars'
    title_page = "Rent " + car_name
        
    if request.method == 'POST':
        form = Rented_CarsForm(request.POST, request.FILES, instance=rentdetails)
        if form.is_valid():
            rented = form.save(commit=False)  
            rented.renters = users
            rented.unit_rented = cars
                
            driver_id = request.POST.get('driver_shp')
            if driver_id: 
                    driver_details = driver_shop.objects.get(id=driver_id)
                    hourly_rate = driver_details.drivers_rate
                    rented.driver_shp = driver_details
            else:
                    hourly_rate = 0
            if rented.pick_up_unit > current_time :
                if rented.return_unit > rented.pick_up_unit:
                        duration = rented.return_unit - rented.pick_up_unit
                else:
                    messages.error(request, "Set time Correctly,please try again")
                    return redirect('rent_vehicles', pk=unit)
            else:
                messages.error(request, "Set time Correctly,please try again")
                return redirect('rent_vehicles', pk=unit)

            total_hours = duration.total_seconds() / 3600

            combine_rate = hourly_rate + car_hourly_rate

            total_cost = combine_rate * total_hours
            rented.total_hrs = total_hours 
            rented.total_fare = total_cost
            rented.save() 
            messages.success(request, "Successfully Transactions")
            return redirect('users')
        else:
            messages.error(request, "Please try again.")
    else:
        form = Rented_CarsForm(instance=rentdetails)
    
    context = {
        'page': page,
        'title_page': title_page,
        'my_shops': my_shops,
        'shop_detail': shop_detail,
        'car_name': car_name,
        'cars': cars,
        'form': form,
        'current_time':current_time,
        'users':users,
    }
    
    return render(request, 'accounts/rent_cars.html', context)


@login_required(login_url='signin')
@role_required(allowed_roles=['2'], redirect_url='admin')
def driverdetails(request,pk):
    users = request.user
    page = ''
    title_page = 'Driver Details'
    driverdet = get_object_or_404(driver_shop,pk=pk)
    my_shops = Shops.objects.filter(owner=users)
    context = {
        'page': page,
        'title_page': title_page,
        'my_shops': my_shops,
        'driverdet':driverdet,
        'users':users,

    }
    return render(request, 'accounts/driverdetails.html', context)


def logoutUser(request):
    user = request.user
    user.log_status = "offline"
    user.save()
    logout(request)
    return redirect('home')



