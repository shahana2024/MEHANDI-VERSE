import smtplib

from django.conf import settings
from django.shortcuts import render
from datetime import datetime, timedelta, date, timezone
import email
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import Group
from django.core.files.storage import FileSystemStorage
from django.db.models import Avg
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q

from myapp.hand_features import extract_hand_features
from myapp.recommend import recommend_designs
from .models import *
# Create your views here.


u=User.objects.get(username="anju@gmail.com")
u.password=make_password("Anju@1234")
u.save()


def forgot_password_get(request):
    return render(request,'forgot_password.html')
def forgot_password(request):
    email=request.POST['email']
    if User.objects.filter(username=email).exists():

        import random
        new_pass = random.randint(00000, 99999)
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login("leagaladvisorteam@gmail.com", " eugnxtyylwtqwlav")  # App Password
        to = email
        subject = "Test Email"
        body = "Your new password is " + str(new_pass)
        msg = f"Subject: {subject}\n\n{body}"
        server.sendmail("s@gmail.com", to, msg)  # Disconnect from the server
        server.quit()

        user = User.objects.get(username=email)
        user.set_password(new_pass)
        user.save()

        return redirect('/myapp/login_get/')
    else:
        messages.warning(request, 'email not  exists')
        return redirect('/myapp/forgot_password/')
def index(request):
    return render(request,'index.html')


def login_get(request):
    return render(request, 'login.html')


def login_post(request):
    uname = request.POST['username']
    pwd = request.POST['password']
    user = authenticate(request, username=uname, password=pwd)
    print("ddddddddddddddd")
    if user is not None:
        login(request, user)
        if user.groups.filter(name='admin').exists():
            messages.success(request, 'Admin Home')
            return redirect('/myapp/admin_home/')
       
        else:
            
            messages.success(request, 'invalid User')
            return redirect('/myapp/login_get/')
    else:
        messages.success(request, 'invalid Username and Password')
        return redirect('/myapp/login_get/')
    
    
def admin_home(request):
    o=Artist.objects.count()
    d=MehndiDesign.objects.count()
    u=USERS.objects.count()
    print("dddddd",o)

    return render(request,'admin_home.html',{"artist": o,"Design":d,"users":u})
def admin_view_artist(request):
    data=Artist.objects.all()
    return render(request,'admin_view_artist.html',{"data":data})
def admin_accept_artist(request,id):
    r=Artist.objects.get(id=id)
    r.status="Accept"
    r.save()
    return redirect('/myapp/admin_view_artist/')
def admin_reject_artist(request,id):
    r=Artist.objects.get(id=id)
    r.status="Reject"
    r.save()
    return redirect('/myapp/admin_view_artist/')

def admin_view_design(request,id):

    o=MehndiDesign.objects.filter(artist_id=id)
    return render(request,'admin_view_design.html',{"data":o})


def admin_view_user(request):
    r=USERS.objects.all()
    return render(request,'admin_view_user.html',{"data":r})


def admin_view_complaints(request):
    u=complaint.objects.all()
    return render(request,'admin_view_complaints.html',{"data":u})
def admin_send_reply(request):
    id=request.POST['id']
    reply=request.POST['reply']
    u=complaint.objects.get(id=id)
    u.reply_text=reply
    u.save()
    return redirect('/myapp/admin_view_complaints/')

def admin_view_feedback(request):
    p=Feedback.objects.all()
    return render(request,'admin_view_feedback.html',{"data":p})

def admin_view_product(request,id):
    o=HennaProduct.objects.filter(artist_id=id)
    return render(request,'admin_view_product.html',{"data":o})
def admin_accept_product(request,id):
    r=HennaProduct.objects.get(id=id)
    r.is_approved='Accept'
    r.save()
    artist_id=r.artist_id
    return redirect(f'/myapp/admin_view_product/{artist_id}')


def admin_reject_product(request,id):
    r=HennaProduct.objects.get(id=id)
    r.is_approved='Reject'
    r.save()
    artist_id=r.artist_id
    return redirect(f'/myapp/admin_view_product/{artist_id}')

def admin_add_recommend_get(request):
    o=Mehndi.objects.all()
    return render(request,'admin_add_recommend.html',{"data":o})
def admin_add_recommend_post(request):
    name=request.POST['name']
    image=request.FILES['image']
    fs = FileSystemStorage()
    filename = fs.save(image.name, image)
    path = fs.url(filename)
    style=request.POST['style']
    palm_width_ratio=request.POST['palm_width_ratio']
    finger_length_ratio=request.POST['finger_length_ratio']
    o=Mehndi(name=name,style=style,palm_width_ratio=palm_width_ratio,finger_length_ratio=
             finger_length_ratio,design_image=path)
    o.save()
    return redirect('/myapp/admin_add_recommend_get/')
def admin_edit_design_get(request,id):
    p=Mehndi.objects.get(id=id)
    return render(request,'admin_edit_design.html',{"data":p})


def admin_edit_design_post(request):
    id = request.POST['id']
    u = Mehndi.objects.get(id=id)
    u.name = request.POST['name']
    u.style = request.POST['style']
    u.finger_length_ratio = request.POST['finger_length_ratio']
    u.palm_width_ratio = request.POST['palm_width_ratio']

    if 'image' in request.FILES and request.FILES['image']:
        image = request.FILES['image']
        fs = FileSystemStorage()
        filename = fs.save(image.name, image)
        path = fs.url(filename)
        u.design_image = path

    u.save()
    return redirect('/myapp/admin_add_recommend_get/')

def admin_delete_design(request,id):
    r=Mehndi.objects.get(id=id)
    r.delete()
    return redirect('/myapp/admin_add_recommend_get/')
























# ============================user============================

from django.contrib.auth import authenticate
from django.http import JsonResponse

from django.contrib.auth import authenticate
from django.http import JsonResponse
from .models import Artist

def userlogin(request):

    if request.method != "POST":
        return JsonResponse({
            'status': 'failed',
            'message': 'Invalid request method'
        })

    username = request.POST.get('username1')
    password = request.POST.get('password')

    user = authenticate(username=username, password=password)

    print("Authenticated User:", user)

    if user is None:
        return JsonResponse({
            'status': 'failed',
            'message': 'Invalid username or password'
        })

    # ✅ Artist Login
    if user.groups.filter(name='artist').exists():

        artist = Artist.objects.filter(LOGIN=user).first()

        if artist and artist.status == "Accept":
            return JsonResponse({
                'status': 'success',
                'message': 'Login successful',
                'group': 'artist',
                'login_id': user.id,
                'name': artist.fname
            })
        else:
            return JsonResponse({
                'status': 'failed',
                'message': 'Artist not approved yet'
            })

    # ✅ Normal User Login
    elif user.groups.filter(name='user').exists():
        o=USERS.objects.get(LOGIN_id=user.id)
        return JsonResponse({
            'status': 'success',
            'message': 'Login successful',
            'group': 'User',
            'name':o.fname,
            'login_id': user.id,
        })

    # ✅ Unknown Group
    else:
        return JsonResponse({
            'status': 'failed',
            'message': 'User group not recognized'
        })

def artist_register(request):
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    email = request.POST['email']
    phone = request.POST['phone']
    address = request.POST['address']
    pincode = request.POST['pincode']
    experience_years = request.POST['experience_years']
    specialization = request.POST['specialization']
    bio = request.POST['bio']
    city = request.POST['city']
    password = request.POST['password']
    profile_image = request.FILES['profile_image']
    fs = FileSystemStorage()
    filename = fs.save(profile_image.name, profile_image)
    profile_image_url = fs.url(filename)
    l = User.objects.create(username=email, password=str(make_password(password)))
    l.groups.add(Group.objects.get(name='artist'))
    l.save()
    artist = Artist.objects.create(
        LOGIN_id=l.id,
        fname=first_name,
        lname=last_name,
        phone=phone,
        profile_image=profile_image_url,
        experience_years=experience_years,
        specialization=specialization,
        bio=bio,
        address=address,
        city=city,
        pincode=pincode,
        email=email
    )
    artist.save()
    response = {
        'status': 'success',
        'message': 'Artist registered successfully'
    }
    return JsonResponse(response)

def user_register(request):
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    email = request.POST['email']
    phone = request.POST['phone']
    address = request.POST['address']
    pincode = request.POST['pincode']
    city = request.POST['city']
    gender = request.POST['gender']
    password = request.POST['password']
    
    l = User.objects.create(username=email, password=str(make_password(password)))
    l.groups.add(Group.objects.get(name='user'))
    l.save()
    user = USERS.objects.create(
        LOGIN_id=l.id,
        fname=first_name,
        lname=last_name,
        phone=phone,
        address=address,
        city=city,
        pincode=pincode,
        email=email,
        gender=gender
    )
    user.save()
    response = {
        'status': 'success',
        'message': 'User registered successfully'
    }
    return JsonResponse(response)


def upload_design(request):

    lid = request.POST['lid']
    image = request.FILES['design_image']
    design_type = request.POST['design_type']
    hand_size = request.POST['hand_size']
    coverage = request.POST['coverage']
    price = request.POST['price']
    
    fs = FileSystemStorage()
    filename = fs.save(image.name, image)
    design_image_url = fs.url(filename)
    i=Artist.objects.get(LOGIN_id=lid)
    artist_id = i.id
    design = MehndiDesign.objects.create(
        artist_id=artist_id,
        image=design_image_url,
        design_type=design_type,
        hand_size=hand_size,
        coverage=coverage,
        price=price,
        date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    design.save()
    
    response = {
        'status': 'success',
        'message': 'Design uploaded successfully'
    }
  
    return JsonResponse(response)
def view_designs(request):
    
    lid= request.POST['lid']
    o=Artist.objects.get(LOGIN_id=lid)
    artist_id=o.id
    designs = MehndiDesign.objects.filter(artist_id=artist_id)
    design_list = []
    for design in designs:
        design_data = {
            'id': design.id,
            'artist_id': design.artist_id,
            'image_url': str(design.image),
            'design_type': design.design_type,
            'hand_size': design.hand_size,
            'coverage': design.coverage,
            'price': str(design.price),
        }
        design_list.append(design_data)
    return JsonResponse({'designs': design_list,'status': 'success'})

def delete_design(request):
    design_id = request.POST['design_id']
    try:
        design = MehndiDesign.objects.get(id=design_id)
        design.delete()
        response = {
            'status': 'success',
            'message': 'Design deleted successfully'
        }
    except MehndiDesign.DoesNotExist:
        response = {
            'status': 'failed',
            'message': 'Design not found'
        }
    return JsonResponse(response)

from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage

def edit_design(request):

    design_id = request.POST.get('design_id')
    design_type = request.POST.get('design_type')
    hand_size = request.POST.get('hand_size')
    coverage = request.POST.get('coverage')
    price = request.POST.get('price')

    try:
        design = MehndiDesign.objects.get(id=design_id)

        # Update normal fields
        design.design_type = design_type
        design.hand_size = hand_size
        design.coverage = coverage
        design.price = price

        # ✅ Check if new image uploaded
        if 'design_image' in request.FILES:
            image = request.FILES['design_image']
            s = FileSystemStorage()
            filename = s.save(image.name, image)
            design.image = s.url(filename)

        design.save()

        response = {
            'status': 'success',
            'message': 'Design updated successfully'
        }

    except MehndiDesign.DoesNotExist:
        response = {
            'status': 'failed',
            'message': 'Design not found'
        }

    return JsonResponse(response)


def add_product(request):
    name=request.POST['name']
    description=request.POST['description']
    price=request.POST['price']
    stock=request.POST['stock']
    image = request.FILES['product_image']

    fs = FileSystemStorage()
    filename = fs.save(image.name, image)
    image_url = fs.url(filename)
    lid=request.POST['lid']
    i=Artist.objects.get(LOGIN_id=lid)
    artist_id=i.id

    product = HennaProduct.objects.create(
        name=name,
        description=description,
        price=price,
        stock=stock,
        image=image_url,
        artist_id=artist_id
    )
    product.save()

    response = {
        'status': 'success',
        'message': 'Product added successfully'
    }
    return JsonResponse(response)

def view_product(request):
    lid= request.POST['lid']
    o=Artist.objects.get(LOGIN_id=lid)
    artist_id=o.id
    products = HennaProduct.objects.filter(artist_id=artist_id)
    product_list = []
    for product in products:
        product_data = {
            'id': product.id,
            'name': product.name,
            'description': product.description,
            'price': str(product.price),
            'stock': product.stock,
            'image_url': str(product.image),
        }
        product_list.append(product_data)
    return JsonResponse({'products': product_list,'status': 'success'})

def delete_product(request):
    product_id = request.POST['product_id']
    try:
        product = HennaProduct.objects.get(id=product_id)
        product.delete()
        response = {
            'status': 'success',
            'message': 'Product deleted successfully'
        }
    except HennaProduct.DoesNotExist:
        response = {
            'status': 'failed',
            'message': 'Product not found'
        }
    return JsonResponse(response)

def edit_product(request):
    product_id = request.POST.get('product_id')
    name = request.POST.get('name')
    description = request.POST.get('description')
    price = request.POST.get('price')
    stock = request.POST.get('stock')

    try:
        product = HennaProduct.objects.get(id=product_id)

        # Update normal fields
        product.name = name
        product.description = description
        product.price = price
        product.stock = stock

        # ✅ Check if new image uploaded
        if 'product_image' in request.FILES:
            image = request.FILES['product_image']
            s = FileSystemStorage()
            filename = s.save(image.name, image)
            product.image = s.url(filename)

        product.save()

        response = {
            'status': 'success',
            'message': 'Product updated successfully'
        }

    except HennaProduct.DoesNotExist:
        response = {
            'status': 'failed',
            'message': 'Product not found'
        }

    return JsonResponse(response)

def view_profile(request):
 
        artist_id = request.POST['lid']
        artist = Artist.objects.get(LOGIN_id=artist_id)
        
        profile_data = {
            'id': artist.id,
            'fname': artist.fname,
            'lname': artist.lname,
            'phone': artist.phone,
            'profile_image':str(artist.profile_image),
            'experience_years': artist.experience_years,
            'specialization': artist.specialization,
            'bio': artist.bio,
            'address': artist.address,
            'city': artist.city,
            'pincode': artist.pincode,
        }
        
        return JsonResponse({
            'status': 'success',
            'profile': profile_data
        })

def update_profile(request):

        artist_id = request.POST['lid']
        artist = Artist.objects.get(LOGIN_id=artist_id)
        artist.fname = request.POST['fname']
        artist.lname = request.POST['lname']
        artist.phone = request.POST['phone']
        artist.experience_years = request.POST['experience_years']
        artist.specialization = request.POST['specialization']
        artist.bio = request.POST['bio']
        artist.address = request.POST['address']
        artist.city = request.POST['city']
        artist.pincode = request.POST['pincode']
        if request.FILES.get('profile_image'):
            image = request.FILES['profile_image']

            fs = FileSystemStorage()
            filename = fs.save(image.name, image)
            image_url = fs.url(filename)
            artist.profile_image = image_url
        
        artist.save()
        
        return JsonResponse({
            'status': 'success',
            'message': 'Profile updated successfully'
        })

def fchange_password_post(request):
    old_password=request.POST['currentpassword']
    new_password=request.POST['newpassword']
    confirm_password=request.POST['confirmpassword']
    lid=request.POST['lid']

    users=User.objects.get(id=lid)

    if check_password(old_password,users.password):
        if new_password==confirm_password:

            users.set_password(new_password)
            users.save()
            return JsonResponse({'status': 'ok'})
        else:
            return JsonResponse({'status': 'No'})
    else:
        return JsonResponse({'status': 'No'}) 
    
    
    
    
    
    
    
    
    
# ==========================user===============================


def view_all_artists(request):
    if request.method == 'POST':
        try:
            artists = Artist.objects.all()
            artist_list = []
            
            for artist in artists:
                artist_data = {
                    'id': artist.id,
                    'fname': artist.fname,
                    'lname': artist.lname,
                    'phone': artist.phone,
                    'profile_image': str(artist.profile_image),
                    'experience_years': artist.experience_years,
                    'specialization': artist.specialization,
                    'bio': artist.bio,
                    'address': artist.address,
                    'city': artist.city,
                    'pincode': artist.pincode,
                }
                artist_list.append(artist_data)
            
            return JsonResponse({
                'status': 'success',
                'artists': artist_list
            })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
def view_gallery(request):
    designs = MehndiDesign.objects.all()
    design_list = []
    for design in designs:
        design_data = {
            'id': design.id,
            'artist_id': design.artist_id,
            'image_url': str(design.image),
            'design_type': design.design_type,
            'hand_size': design.hand_size,
            'coverage': design.coverage,
            'price': str(design.price),
        }
        design_list.append(design_data)
    return JsonResponse({'designs': design_list,'status': 'success'})


# views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from django.utils import timezone
from .models import Chat, Artist, User
import os


def userview_chat(request, id1, id2):

    artist = Artist.objects.get(id=id2)
    login1 = artist.LOGIN_id

    # Get user Login
    login2 = id1

    # Get chat between these two login users
    messages = Chat.objects.filter(
        sender__in=[login1, login2],
        receiver__in=[login1, login2]
    ).order_by('id')

    data = []
    for msg in messages:
        message_data = {
            'id': msg.id,
            'sender_id': msg.sender.id,
            'receiver_id': msg.receiver.id,
            'message': msg.message,
            'date': msg.timestamp,
            'message_type': msg.message_type,
        }

        # Add image URL if it's an image message
        if msg.message_type == 'image' and msg.image:
            message_data['image_url'] = msg.image

        data.append(message_data)

    return JsonResponse({'status': 'success', 'data': data})




def usersend_chat(request):

    sender_id = request.POST.get('sender_id')
    receiver_artist_id = request.POST.get('receiver_id')
    content = request.POST.get('chat', '')
    message_type = request.POST.get('message_type', 'text')

    # Get sender's Login
    sender = User.objects.get(id=sender_id)
    sender_login = sender_id

    # Get receiver's Login
    receiver_artist = Artist.objects.get(id=receiver_artist_id)
    receiver_login = receiver_artist.LOGIN_id

    # Create new message
    new_message = Chat(
        sender_id=sender_login,
        receiver_id=receiver_login,
        message=content,
        timestamp=timezone.now(),
        message_type=message_type
    )
    new_message.save()

    return JsonResponse({
        'status': 'success',
        'message': 'Message sent successfully',
        'message_id': new_message.id
    })




def usersend_chat_image(request):

    sender_id = request.POST.get('sender_id')
    receiver_artist_id = request.POST.get('receiver_id')
    content = request.POST.get('chat', '')
    message_type = request.POST.get('message_type', 'image')

    # Get sender's Login
    sender = User.objects.get(id=sender_id)
    sender_login = sender_id

    # Get receiver's Login
    receiver_artist = Artist.objects.get(id=receiver_artist_id)
    receiver_login = receiver_artist.LOGIN_id

    # Handle image upload
    image_file = request.FILES.get('chat_image')
    image_url = None

    if image_file:
        # Save image
        fs = FileSystemStorage()
        filename = fs.save(image_file.name, image_file)
        image_url = fs.url(filename)

    # Create new message with image
    new_message = Chat(
        sender_id=sender_login,
        receiver_id=receiver_login,
        message=content,
        timestamp=timezone.now(),
        message_type=message_type,
        image=image_url
    )
    new_message.save()

    return JsonResponse({
        'status': 'success',
        'message': 'Image sent successfully',
        'message_id': new_message.id,
        'image_url': str(new_message.image)
    })



def send_booking_request(request):
    user_id = request.POST['user_id']
    artist_id = request.POST['artist_id']
    booking_date = request.POST['booking_date']
    booking_time = request.POST['booking_time']

    
    user = USERS.objects.get(LOGIN_id=user_id)
    artist = Artist.objects.get(id=artist_id)

    booking = Booking.objects.create(
        user=user,
        artist=artist,
        booking_date=booking_date,
        booking_time=booking_time
    )
    booking.save()

    response = {
        'status': 'success',
        'message': 'Booking created successfully'
    }


    return JsonResponse(response)



def user_view_products(request):

    products = HennaProduct.objects.filter(is_approved='Accept')
    product_list = []
    print ("ddddddddd",product_list)
    
    for product in products:
        product_data = {
            'id': product.id,
            'name': product.name,
            'arti_name': product.artist.fname,
            'description': product.description,
            'price': str(product.price),
            'stock': product.stock,
            'image_url': str(product.image),
            'is_approved': product.is_approved,
            'created_at': product.created_at.isoformat(),
            'artist_id': product.artist_id,
        }
        product_list.append(product_data)
    
    return JsonResponse({
        'status': 'success',
        'products': product_list
    })
   


def place_order(request):
    product_id = request.POST.get('product_id')
    lid = request.POST.get('user_id')
    quantity = int(request.POST.get('quantity', 1))
    total_price = float(request.POST.get('total_price', 0))
    status = request.POST.get('status', 'pending')
    payment_id = request.POST.get('payment_id', '')
    payment_status = request.POST.get('payment_status', 'pending')
    payment_method = request.POST.get('payment_method', 'COD')
    i=USERS.objects.get(LOGIN_id=lid)
    user_id = i.id
    # Validate product exists and has sufficient stock
    try:
        product = HennaProduct.objects.get(id=product_id)
    except HennaProduct.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Product not found'})

    # Check stock availability
    if product.stock < quantity:
        return JsonResponse({
            'status': 'error', 
            'message': f'Insufficient stock. Available: {product.stock}'
        })

    # Create order with payment details
    order = Order.objects.create(
        quantity=quantity,
        total_price=total_price,
        order_date=datetime.now(),
        status='Paid' if payment_status == 'success' else 'Pending',
        product_id=product.id,
        user_id=user_id,
     
    )

    # Update product stock
    product.stock -= quantity
    product.save()

    return JsonResponse({
        'status': 'success',
        'message': 'Order placed successfully',
        'order_id': order.id
    })
    
    

def view_bookings(request):
    lid= request.POST.get('user_id')
    i=USERS.objects.get(LOGIN_id=lid)
    user_id = i.id
    
    orders = Order.objects.filter(user_id=user_id).order_by('-order_date')
    
    booking_list = []
    for order in orders:
        try:
            product = HennaProduct.objects.get(id=order.product_id)
            product_name = product.name
            product_price = float(product.price)
            product_image = str(product.image)
        except HennaProduct.DoesNotExist:
            product_name = 'Unknown Product'
            product_price = 0
            product_image = ''
        
        booking_data = {
            'id': order.id,
            'quantity': order.quantity,
            'total_price': str(order.total_price),
            'order_date': order.order_date.isoformat(),
            'status': order.status,
            'product_id': order.product_id,
            'product_name': product_name,
            'product_image': product_image,
            'product_price': str(product_price),
        }
        booking_list.append(booking_data)
    
    return JsonResponse({
        'status': 'success',
        'bookings': booking_list
    })



def view_artist_bookings(request):
    user_lid = request.POST.get('lid')
    user = USERS.objects.get(LOGIN_id=user_lid)
    user_id = user.id
    bookings = Booking.objects.filter(user_id=user_id).order_by('-created_at')
    
    booking_list = []
    for booking in bookings:
        artist = Artist.objects.get(id=booking.artist_id)
        
        # Get feedback for this booking if exists
        feedback_data = None
        try:
            # If using OneToOneField with related_name='feedback'
            if hasattr(booking, 'feedback'):
                feedback = booking.feedback
                feedback_data = {
                    'id': feedback.id,
                    'rating': feedback.rating,
                    'comment': feedback.comment,
                    'created_at': feedback.created_at.isoformat(),
                    'booking_id': booking.id,
                }
        except:
            # If using a separate model with booking_id field
            try:
                from .models import Feedback
                feedback = Feedback.objects.get(booking_id=booking.id)
                feedback_data = {
                    'id': feedback.id,
                    'rating': feedback.rating,
                    'comment': feedback.comment,
                    'created_at': feedback.created_at.isoformat(),
                    'booking_id': booking.id,
                }
            except:
                pass
        
        booking_data = {
            'id': booking.id,
            'booking_date': booking.booking_date.isoformat(),
            'booking_time': booking.booking_time,
            'status': booking.status,
            'created_at': booking.created_at.isoformat(),
            'artist_id': booking.artist_id,
            'user_id': booking.user_id,
            'user_fname': artist.fname,
            'user_lname': artist.lname,
            'user_phone': artist.phone,
            'user_profile_image': str(artist.profile_image),
            'amount': str(booking.amount) if hasattr(booking, 'amount') else '0',
            'feedback': feedback_data,  # Include feedback data
        }
        booking_list.append(booking_data)
    
    return JsonResponse({
        'status': 'success',
        'bookings': booking_list
    })

def update_booking_status(request):
    booking_id = request.POST.get('booking_id')
    status = request.POST.get('status')
    
    booking = Booking.objects.get(id=booking_id)
    booking.status = status
    booking.save()
    
    return JsonResponse({
        'status': 'success',
        'message': f'Booking {status} successfully'
    })

def payment_success(request):
    booking_id = request.POST.get('booking_id')
    payment_id = request.POST.get('payment_id')
    
    
    booking = Booking.objects.get(id=booking_id)
    booking.status = 'paid'
    booking.payment_id = payment_id
    booking.payment_date = datetime.now()
    booking.save()
    
    return JsonResponse({
        'status': 'success',
        'message': 'Payment recorded successfully'
    })
    
def submit_feedback(request):
    booking_id = request.POST.get('booking_id')
    rating = request.POST.get('rating')
    comment = request.POST.get('comment', '')
    
    booking = Booking.objects.get(id=booking_id)
    
    feedback = Feedback.objects.create(
        booking=booking,
        rating=rating,
        comment=comment
    )
    feedback.save()
    
    return JsonResponse({
        'status': 'success',
        'message': 'Feedback submitted successfully'
    })
       

# views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from .models import USERS
import os


@csrf_exempt
def artiview_profile(request):
    lid = request.POST.get('lid')
    print("llllllll", lid)
    user = Artist.objects.get(LOGIN_id=lid)

    profile_data = {
        'id': user.id,
        'fname': user.fname,
        'lname': user.lname,
        'phone': user.phone,
        'address': user.address,
        'pincode': user.pincode,
        'city': user.city,
        'profile_image': str(user.profile_image),
        'experience_years': user.experience_years,
        'specialization': user.specialization,
        'bio': user.bio,
        'status': user.status
    }

    return JsonResponse({
        'status': 'success',
        'profile': profile_data
    })


@csrf_exempt
def view_profile(request):
    lid = request.POST.get('lid')
    print("llllllll", lid)
    user = USERS.objects.get(LOGIN_id=lid)

    profile_data = {
        'id': user.id,
        'fname': user.fname,
        'lname': user.lname,
        'phone': user.phone,
        'address': user.address,
        'pincode': user.pincode,
        'city': user.city,
        'gender': user.gender,
    }

    return JsonResponse({
        'status': 'success',
        'profile': profile_data
    })


def userupdate_profile(request):
    lid = request.POST.get('lid')
    user = USERS.objects.get(LOGIN_id=lid)

    # Update fields
    user.fname = request.POST.get('fname', user.fname)
    user.lname = request.POST.get('lname', user.lname)
    user.phone = request.POST.get('phone', user.phone)
    user.address = request.POST.get('address', user.address)
    user.pincode = request.POST.get('pincode', user.pincode)
    user.city = request.POST.get('city', user.city)
    user.gender = request.POST.get('gender', user.gender)



    user.save()

    return JsonResponse({
        'status': 'success',
        'message': 'Profile updated successfully'
    })


def update_profile(request):

    lid = request.POST.get('lid')
    user = Artist.objects.get(LOGIN_id=lid)
    
    # Update fields
    user.fname = request.POST.get('fname', user.fname)
    user.lname = request.POST.get('lname', user.lname)
    user.phone = request.POST.get('phone', user.phone)
    user.address = request.POST.get('address', user.address)
    user.pincode = request.POST.get('pincode', user.pincode)
    user.city = request.POST.get('city', user.city)

    # Handle profile image
    if request.FILES.get('profile_image'):
        # Delete old image

        
        # Save new image
        image_file = request.FILES['profile_image']
        fs = FileSystemStorage()
        filename = fs.save(image_file.name, image_file)
        image_url = fs.url(filename)
        user.profile_image=image_url
    
    user.save()
    
    return JsonResponse({
        'status': 'success',
        'message': 'Profile updated successfully'
    })
    


from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os

def recommend_mehndi(request):

    if request.method == "POST" and request.FILES.get("hand_image"):

        image = request.FILES["hand_image"]

        fs = FileSystemStorage()
        filename = fs.save(image.name, image)
        file_path = os.path.join(settings.MEDIA_ROOT, filename)

        features = extract_hand_features(file_path)

        if not features:
            return JsonResponse({"status": "error", "message": "No hand detected"})

        top_designs = recommend_designs(features)

        result = []
        for design in top_designs:

            image_url = None
            if design.design_image:
                image_url = str(design.design_image)

            result.append({
                "name": design.name,
                "style": design.style,
                "image": image_url,
            })

        print("Top designs:", result)

        return JsonResponse({
            "status": "success",
            "recommendations": result
        })

    return JsonResponse({"status": "error", "message": "Invalid request"})



def view_complaints(request):
    lid = request.POST.get('user_id')
    o = USERS.objects.get(LOGIN_id=lid)
    user_id = o.id
    complaints = complaint.objects.filter(user_id=user_id).order_by('-created_at')
    
    complaint_list = []
    for complaints in complaints:
        complaint_data = {
            'id': complaints.id,
            'complaint_text': complaints.complaint_text,
            'reply_text': complaints.reply_text,
            'created_at': complaints.created_at.isoformat(),
            'user_id': complaints.user_id,
        }
        complaint_list.append(complaint_data)
    
    return JsonResponse({
        'status': 'success',
        'complaints': complaint_list
    })
    

def send_complaint(request):
    lid= request.POST.get('user_id')
    o=USERS.objects.get(LOGIN_id=lid)
    user_id = o.id
    complaint_text = request.POST.get('complaint_text')
    
    complaints = complaint.objects.create(
        user_id=user_id,
        complaint_text=complaint_text,
        created_at=datetime.now(),
    reply_text='pending'
    )
    
    return JsonResponse({
        'status': 'success',
        'message': 'Complaint sent successfully',
        'complaint_id': complaints.id
    })
        

def reply_complaint(request):

    complaint_id = request.POST.get('complaint_id')
    reply_text = request.POST.get('reply_text')
    
    complaint = complaint.objects.get(id=complaint_id)
    complaint.reply_text = reply_text
    complaint.save()
    
    return JsonResponse({
        'status': 'success',
        'message': 'Reply sent successfully'
    })


def view_artist_requests(request):

    lid = request.POST.get('artist_id')
    u=Artist.objects.get(LOGIN_id=lid)
    artist_id=u.id
    bookings = Booking.objects.filter(artist_id=artist_id).order_by('-created_at')

    request_list = []
    for booking in bookings:
        user = USERS.objects.get(id=booking.user_id)
        request_data = {
            'id': booking.id,
            'booking_date': booking.booking_date.isoformat(),
            'booking_time': booking.booking_time,
            'status': booking.status,
            'created_at': booking.created_at.isoformat(),
            'artist_id': booking.artist_id,
            'user_id': booking.user_id,
            'amount': str(booking.amount) if hasattr(booking, 'amount') else '0',
            'user_fname': user.fname,
            'user_lname': user.lname,
            'user_phone': user.phone,

        }
        request_list.append(request_data)

    return JsonResponse({
        'status': 'success',
        'requests': request_list
    })



def update_request_amount(request):

    request_id = request.POST.get('request_id')
    amount = request.POST.get('amount')

    booking = Booking.objects.get(id=request_id)
    booking.amount = amount
    booking.save()

    return JsonResponse({
        'status': 'success',
        'message': 'Amount updated successfully'
    })



def update_request_status(request):

    request_id = request.POST.get('request_id')
    status = request.POST.get('status')

    booking = Booking.objects.get(id=request_id)
    booking.status = status
    booking.save()

    return JsonResponse({
        'status': 'success',
        'message': f'Request {status} successfully'
    })


def arti_view_chat(request, id1, id2):

    # Get Artist and their Login
    artist = USERS.objects.get(id=id2)
    login1 = artist.LOGIN_id

    # Get user Login
    login2 = id1

    # Get chat between these two login users
    messages = Chat.objects.filter(
        sender__in=[login1, login2],
        receiver__in=[login1, login2]
    ).order_by('id')

    data = []
    for msg in messages:
        message_data = {
            'id': msg.id,
            'sender_id': msg.sender.id,
            'receiver_id': msg.receiver.id,
            'message': msg.message,
            'date': msg.timestamp,
            'message_type': msg.message_type,
        }

        # Add image URL if it's an image message
        if msg.message_type == 'image' and msg.image:
            message_data['image_url'] = msg.image

        data.append(message_data)

    return JsonResponse({'status': 'success', 'data': data})




@csrf_exempt
def arti_send_chat(request):

            sender_id = request.POST.get('sender_id')
            receiver_user_id = request.POST.get('receiver_id')
            content = request.POST.get('chat', '')
            message_type = request.POST.get('message_type', 'text')

            # Get receiver's login ID
            receiver = USERS.objects.get(id=receiver_user_id)
            receiver_login = receiver.LOGIN_id

            # Create new message
            new_message = Chat(
                sender_id=sender_id,
                receiver_id=receiver_login,
                message=content,
                timestamp=datetime.now(),
                message_type=message_type
            )
            new_message.save()

            return JsonResponse({
                'status': 'success',
                'message': 'Message sent successfully',
                'message_id': new_message.id
            })

def arti_send_chat_image(request):

    sender_id = request.POST.get('sender_id')
    receiver_user_id = request.POST.get('receiver_id')
    content = request.POST.get('chat', '')
    message_type = request.POST.get('message_type', 'image')

    # Get receiver's login ID
    receiver = USERS.objects.get(id=receiver_user_id)
    receiver_login = receiver.LOGIN_id

    # Handle image upload
    image_file = request.FILES.get('chat_image')
    image_url = None

    if image_file:
        # Save image
        fs = FileSystemStorage()
        filename = fs.save(image_file.name, image_file)
        image_url = fs.url(filename)

    # Create new message with image
    new_message = Chat(
        sender_id=sender_id,
        receiver_id=receiver_login,
        message=content,
        timestamp=datetime.now(),
        message_type=message_type,
        image=image_url
    )
    new_message.save()

    return JsonResponse({
        'status': 'success',
        'message': 'Image sent successfully',
        'message_id': new_message.id,
        'image_url': str(new_message.image)
    })





def view_product_orders(request):

    p = request.POST.get('artist_id')
    a=Artist.objects.get(LOGIN_id=p)
    artist_id=a.id

    # Get all orders for products belonging to this artist
    # Assuming products have artist_id field
    products = HennaProduct.objects.filter(artist_id=artist_id)
    product_ids = [p.id for p in products]

    orders = Order.objects.filter(product_id__in=product_ids).order_by('-order_date')

    order_list = []
    for order in orders:
        product = HennaProduct.objects.get(id=order.product_id)
        user = USERS.objects.get(id=order.user_id)

        order_data = {
            'id': order.id,
            'quantity': order.quantity,
            'total_price': str(order.total_price),
            'order_date': order.order_date.isoformat(),
            'status': order.status,
            'product_id': order.product_id,
            'user_id': order.user_id,
            'product_name': product.name,
            'product_image': str(product.image),
            'product_price': str(product.price),
            'user_fname': user.fname,
            'user_lname': user.lname,
            'user_phone': user.phone,

        }
        order_list.append(order_data)

    return JsonResponse({
        'status': 'success',
        'orders': order_list
    })




def update_order_status(request):

    order_id = request.POST.get('order_id')
    status = request.POST.get('status')

    order = Order.objects.get(id=order_id)
    order.status = status
    order.save()

    return JsonResponse({
        'status': 'success',
        'message': f'Order status updated to {status}'
    })
