from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *

# Create your views here.

current_user = ''

def home(request):
    return render(request,'home.html')

def register(request):
    print(request.method)
    if request.method == "POST":
        name = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password')
        password2 = request.POST.get('password2')
        print(name,email,password1,password2)
        if(password1 == password2):
            user = User(username=name,password=password1,email=email)
            user.save()
            return redirect('/home')
        else:
            return render(request, 'register.html')
        
    else:
        print("bye")
        return render(request,'register.html')

def login(request):
    global current_user

    if current_user != '':
        return redirect('/dashboard')

    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        if(email == "admin@gmail.com" and password == "123"):
            current_user = 'admin'
            return redirect('/adminpanel')

        if User.objects.filter(email=email).exists():
            print('yes')
            l = User.objects.filter(email=email).values_list()
            if l[0][2] == password:
                print('double yes')
                current_user = l[0][1]
                return redirect('/dashboard')
        else:
            print('no')
    else:
        return render(request, 'login.html')

def logout(request):
    global current_user
    current_user = ''
    return redirect('/home')

def dashboard(request):
    global current_user
    if current_user == '':
        return redirect('home')
    
    center = Center.objects.all().values_list()
    centers = Center.objects.all().values()
    slots = {}
    for i in center:
        temp = i[1]
        my_center = Center.objects.get(id=i[0])
        slots[temp] = my_center.get_slots_count()

    user_instance = User.objects.get(username=current_user)
    user_slots = Slot.objects.filter(username=user_instance).values()
    print(user_slots)

    context = {
        'user':current_user,
        'center':centers,
        'slots':slots,
        'userslots':user_slots,
    }
    return render(request, 'dashboard.html', context)
    

def seperate(request, pk):
    center_data = Center.objects.filter(id=pk).values()
    my_center = Center.objects.get(id=pk)
    slot_count = my_center.get_slots_count()
    slots = Slot.objects.filter(name=my_center)

    context = {
        'center_data': center_data,
        'slot_count': slot_count,
        'slots':slots,
    }
    
    if request.method == "POST":
        slot_id_to_book = request.POST.get('slot_id')
        global current_user
        try:
            user = User.objects.get(username=current_user)
            slot_to_book = Slot.objects.get(id=slot_id_to_book, name=my_center, username=None)
            slot_to_book.username = user
            slot_to_book.save()
            print(f"Slot {slot_id_to_book} booked by {user}")
            return redirect('seperate', pk=pk)
        except Slot.DoesNotExist:
            print(f"Slot {slot_id_to_book} is not available or already booked")


    return render(request, 'seperate.html', context)


def adminpanel(request):
    global current_user
    if(current_user != 'admin'):
        return redirect('/home')
    center = Center.objects.all().values_list()
    centers = Center.objects.all().values()
    slots = {}
    for i in center:
        temp = i[1]
        my_center = Center.objects.get(id=i[0])
        slots[temp] = my_center.get_slots_count()
    
    if request.method == 'POST':
        name = request.POST.get('name')
        location = request.POST.get('location')
        address = request.POST.get('address')
        new_center = Center(name=name, location=location, address=address)
        new_center.save()

        print(f"Center {name} added by admin")
        return redirect('adminpanel')

    context = {
        'center':centers,
        'slots':slots,
    }

    return render(request,"adminpanel.html",context)

def delete_center(request, center_id):
    global current_user
    if current_user != 'admin':
        return redirect('/home')

    try:
        centerdelete = Center.objects.get(id=center_id)
        centerdelete.delete()
        print(f"Center {center_id} deleted by admin")
    except Center.DoesNotExist:
        print(f"Center {center_id} not found")

    return redirect('adminpanel')

def addslot(request):
    global current_user
    if current_user != 'admin':
        return redirect('/home')
    
    if(request.method == "POST"):
        name = request.POST.get('name')
        name.strip()
        timing = request.POST.get('timing')
        print(name,timing)
        center_name = Center.objects.get(name=name)
        new_center = Slot(name=center_name, timings=timing, username=None)
        new_center.save()
        return redirect('/adminpanel')


    return redirect('/adminpanel')