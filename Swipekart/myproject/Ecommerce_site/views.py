from django.shortcuts import render,redirect
from . models import *
from django.contrib import messages
from django.shortcuts import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserForm
from django.http import JsonResponse
import json
# Create your views here.

def home(request):
    products=Product.objects.filter(trending=1)
    return render(request,'html/home.html',{"products":products})

def register(request):
    form = CustomUserForm()
    if request.method=='POST':
        form=CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Registration Success You can Log in")
            return redirect("login")
    return render(request, 'html/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('/home')
    else:
        if request.method== 'POST':
            name=request.POST.get('username')
            pwd=request.POST.get('password')
            user=authenticate(request,username=name,password=pwd)
            if user is not None:
                login(request,user)
                messages.success(request,"Logged in Successfully")
                return redirect('/home')
            else:
                messages.error(request,"Invalid Username or Password")
                return redirect('/login')
        return render(request,'html/login.html')

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,"Logged out Succesfully")
    return redirect('/home')
    
def collections(request):
    category=Category.objects.filter(status=0)
    return render(request,'html/collections.html',{"category":category})

def collections_view(request,name):
    if(Category.objects.filter(name=name)):
        products=Product.objects.filter(catagory__name=name)
        return render(request,'html/collectionsview.html',{"products":products,"category_name":name})
    else:
        messages.warning(request,"No such category found")
        return redirect('collections_views')

def product_details(request,cname,pname):
    if(Category.objects.filter(name=cname,status=0)):
        if(Product.objects.filter(name=pname,status=0)):
            products=Product.objects.filter(name=pname,status=0).first()
            return render(request,'html/productdetails.html',{"products":products})
        else:
            messages.error(request,"No such Category Found")
            return redirect("collections")
    else:
        messages.error(request,"No Such Product Found")
        return redirect("collections")
    
def add_to_cart(request):
    if request.headers.get('x-requested-with')=='XMLHttpRequest':
        if request.user.is_authenticated:
            data=json.load(request)
            product_qty=data['product_qty']
            product_id=data['pid']
            #print(request.user.id)

            product_status=Product.objects.get(id=product_id)
            if product_status:
                if Cart.objects.filter(user=request.user.id,product_id=product_id):
                    return JsonResponse({'status':'Product Already in Cart'}, status=200)
                else:
                    if product_status.quantity>=product_qty:
                        Cart.objects.create(user=request.user,product_id=product_id,product_qty=product_qty)
                        return JsonResponse({'status':'Product Added in Cart'},status=200)
                        #return messages.success(request,"Product Added successfully")

                    else:
                        return JsonResponse({'status':'Product Stock not available'},status=200)
        else:
            return JsonResponse({'status':'Login to Add Cart'}, status=200)
    else:
        return JsonResponse({'status':'Invalid Access'}, status=200)\
        
def cart_page(request):
    if request.user.is_authenticated:
        cart=Cart.objects.filter(user=request.user)
        return render(request,'html/cart.html',{"cart":cart})
    else:
        return redirect('/home')
    
def remove_cart(request,cid):
    cartitem=Cart.objects.get(id=cid)
    cartitem.delete()
    return redirect('/cart')
