

#from http.client import HTTPResponse
from django.shortcuts import render,redirect
from . models import *

from django.contrib import messages
from shop.forms import CustomUserForm
from django.contrib.auth import authenticate,login,logout
from django.http import JsonResponse
import json
# Create your views here.
def home(request):
    products=Products.objects.filter(trending=1)
    context={
        'data':products
    }
    return render(request,'shop/index.html',context)

def login_page(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:

        if request.method=='POST':
            name=request.POST.get('username')
            pswd=request.POST.get('password')
            user=authenticate(request,username=name,password=pswd)
            if user is not None:
                login(request,user)
                messages.success(request,'Logged in successfully')
                return redirect('/')
        return render(request,'shop/login.html')

def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,'User Logged out successfully')
    return redirect('/')

def register(request):
    form=CustomUserForm
    if request.method=='POST':
        form=CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Registration was success you can Login Now...!')
            return redirect('/login')
    
    return render(request,'shop/register.html',{ 'data':form })

def collections(request):
    category=Category.objects.filter(status=0)
    context={
        'data': category
    }
    return render(request,'shop/collections.html',context)

def collectionview(request,name):
    if(Category.objects.filter(name=name,status=0)):
        products=Products.objects.filter(category__name=name)
        context={
            'data1': products,
            'data2': name
        }
        return render(request,'shop/products/index.html',context)
    else:
        messages.warning(request,"No such Category found")
        return redirect('collection')

def product_details(request,cname,pname):
    #return redirect('collection')
    #return render(request,'shop/product_details.html')
    if (Category.objects.filter(name=cname,status=0)):
        if(Products.objects.filter(name=pname,status=0)):
            products=Products.objects.filter(name=pname,status=0).first()
            return render(request,'shop/products/product_details.html',{'data':products})
        else:
            messages.error(request,'No such Product found')
            return redirect('collection')
    else:
        messages.error(request,'No such category found')
        return redirect('collection')

def add_to_cart(request):
    if request.headers.get('X-requested-with')=='XMLHttpRequest':
        if request.user.is_authenticated:
            data=json.load(request)
            product_quantity=data['product_qty'] #print('product Quantity ',data['product_qty'])
            product_id=data['pid']             #print('product id is ',data['pid'])
            product_status=Products.objects.get(id=product_id)             #print('User id is ',request.user.id)
            if product_status:
                if Cart.objects.filter(user=request.user, products_id=product_id):
                    return JsonResponse({'status': 'Product already in Cart'}, status=200)
                else:
                    if product_status.quantity >= product_quantity:
                        Cart.objects.create(user=request.user, products_id=product_id, product_qty=product_quantity)
                        return JsonResponse({'status':'Product added to Cart success'}, status=200)
                    else:
                        return JsonResponse({'status': 'Product stock not available'}, status=200)
        else:
            return JsonResponse({'status': 'Login to add Cart'})
    else:
        return JsonResponse({'status':'invalid Access'}, status=200)
def cart_page(request):
    if request.user.is_authenticated:
        cart=Cart.objects.filter(user=request.user)
        return render(request,'shop/cart.html',{'data': cart})
    else:
        return redirect('/')

def remove_cart(request,cid):
    cartitem=Cart.objects.get(id=cid)
    cartitem.delete()
    return redirect('/cart')

def fav_items(request):
    if request.headers.get('x-requested-with')=='XMLHttpRequest':
        if request.user.is_authenticated:
            data=json.load(request)
            product_id=data['pid']
            product_status=Products.objects.get(id=product_id)
            if product_status:
                if Favourite.objects.filter(user=request.user.id, product_id=product_id):
                    return JsonResponse({'status': 'Product Already in Favourite'})
                else:
                    Favourite.objects.create(user=request.user,product_id=product_id)
                    return JsonResponse({'status': 'Product added to favourite'})
        else:
            return JsonResponse({'status': 'Login to Add Favourite'}, status=200)
    else:
        return JsonResponse({'status':'Invalid Access'}, status=200)

def fav_page(request):
    if request.user.is_authenticated:
        fav=Favourite.objects.filter(user=request.user)
        return render(request,'shop/fav.html',{'data': fav })
    else:
        return redirect('/')

def un_fav(request,fid):
    favitems=Favourite.objects.get(id=fid)
    favitems.delete()
    return redirect('favpage')