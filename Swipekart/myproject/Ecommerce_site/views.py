from django.shortcuts import render,redirect
from . models import *
from django.contrib import messages
from django.shortcuts import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserForm
from django.http import JsonResponse
import json
from django.shortcuts import get_object_or_404
from .models import Address
from .forms import AddressForm
from django.db import transaction
from django.template.loader import get_template
from xhtml2pdf import pisa

from .models import Cart, Address, Order, OrderItem   # make sure Order/OrderItem exist
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
        return redirect('home')
    else:
        if request.method== 'POST':
            name=request.POST.get('username')
            pwd=request.POST.get('password')
            user=authenticate(request,username=name,password=pwd)
            if user is not None:
                login(request,user)
                messages.success(request,"Logged in Successfully")
                return redirect('home')
            else:
                messages.error(request,"Invalid Username or Password")
                return redirect('login')
        return render(request,'html/login.html')

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,"Logged out Succesfully")
    return redirect('home')
    
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

def checkout(request):
    return render(request,'html/checkout.html',)
    #return messages.success(request,'ThankYou for Purchasing with Swipekart...!')

def profile_view(request):
    addresses = Address.objects.filter(user=request.user)
    return render(request, 'html/profile.html', {'addresses': addresses})

def add_address(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            return redirect('profile')
    else:
        form = AddressForm()
    return render(request, 'html/address_form.html', {'form': form})

def edit_address(request, id):
    address = get_object_or_404(Address, id=id, user=request.user)
    if request.method == 'POST':
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = AddressForm(instance=address)
    return render(request, 'html/address_form.html', {'form': form})

def delete_address(request, id):
    address = get_object_or_404(Address, id=id, user=request.user)
    address.delete()
    return redirect('profile')

def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)
    addresses = Address.objects.filter(user=request.user)
    return render(request, 'html/checkout.html', {'cart': cart_items, 'addresses': addresses})

@login_required
def checkout(request):
    """Show address list, payment options and cart preview."""
    cart_items = Cart.objects.select_related('product').filter(user=request.user)
    if not cart_items.exists():
        messages.info(request, "Your cart is empty.")
        return redirect('cart')        # tweak to your cart‑view URL

    addresses = Address.objects.filter(user=request.user)
    return render(
        request,'html/checkout.html',{'cart': cart_items,'addresses': addresses,})


@login_required
@transaction.atomic
def place_order(request):
    """Convert the cart into an Order + OrderItems, then clear the cart."""
    if request.method != 'POST':
        return redirect('checkout')

    # ----------------------------- 1. Validate form input ------------------- #
    address_id = request.POST.get('selected_address')
    payment_method = request.POST.get('payment_method')

    if not address_id:
        messages.error(request, "Please choose a delivery address.")
        return redirect('checkout')
    if not payment_method:
        messages.error(request, "Please choose a payment method.")
        return redirect('checkout')

    address = get_object_or_404(Address, id=address_id, user=request.user)
    cart_items = Cart.objects.select_related('product').filter(user=request.user)
    if not cart_items.exists():
        messages.error(request, "Your cart is empty.")
        return redirect('checkout')

    # Create the order
    order_total = sum(item.total_cost for item in cart_items)

    order = Order.objects.create(user=request.user,address=address,payment_method=payment_method,total_amount=order_total,status='Confirmed') # or whatever default you use

    # Order items
    OrderItem.objects.bulk_create([
        OrderItem(order=order,product=item.product,quantity=item.product_qty,price=item.product.selling_price,subtotal=item.total_cost)
        for item in cart_items])
    cart_items.delete()
    messages.success(request, "Order placed successfully! 🎉")
    return redirect('order_success', order_id=order.id)

@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'html/order_success.html', {'order': order})

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'html/my_orders.html', {'orders': orders})

@login_required
def download_invoice(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    template_path = 'html/invoice_template.html'
    context = {'order': order}

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{order.id}.pdf"'

    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('Invoice generation failed', status=500)
    return response