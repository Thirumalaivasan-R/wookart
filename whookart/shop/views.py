import uuid
from django.http import  HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from . models import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .form import ChangePasswordForm, CustomUserForm, EditProfileForm,EmailChangeForm
import json
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
 
 
def home(request):
  products=Product.objects.filter(trending=1)
  return render(request,"shop/index.html",{"products":products})

def fav_page(request):
   if request.headers.get('x-requested-with')=='XMLHttpRequest':
    if request.user.is_authenticated:
      data=json.load(request)
      product_id=data['pid']
      product_status=Product.objects.get(id=product_id)
      if product_status:
         if Favourite.objects.filter(user=request.user.id,product_id=product_id):
          return JsonResponse({'status':'Product Already in Favourite'}, status=200)
         else:
          Favourite.objects.create(user=request.user,product_id=product_id)
          return JsonResponse({'status':'Product Added to Favourite'}, status=200)
    else:
      return JsonResponse({'status':'Login to Add Favourite'}, status=200)
   else:
    return JsonResponse({'status':'Invalid Access'}, status=200)
 
def favviewpage(request):
  if request.user.is_authenticated:
    fav=Favourite.objects.filter(user=request.user)
    return render(request,"shop/fav.html",{"fav":fav})
  else:
    return redirect("login")
 
def remove_fav(request,fid):
  item=Favourite.objects.get(id=fid)
  item.delete()
  return redirect("/favviewpage")
 
 
def cart_page(request):
  if request.user.is_authenticated:
    cart=Cart.objects.filter(user=request.user)
    return render(request,"shop/cart.html",{"cart":cart})
  else:
    return redirect("login")
 
def remove_cart(request,cid):
  cartitem=Cart.objects.get(id=cid)
  cartitem.delete()
  return redirect("/cart")
 
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
            return JsonResponse({'status':'Product Added to Cart'}, status=200)
          else:
            return JsonResponse({'status':'Product Stock Not Available'}, status=200)
    else:
      return JsonResponse({'status':'Login to Add Cart'}, status=200)
   else:
    return JsonResponse({'status':'Invalid Access'}, status=200)
 
def logout_page(request):
  if request.user.is_authenticated:
    logout(request)
    messages.success(request,"Logged out Successfully")
  return redirect("/")

def login_page(request):
  if request.user.is_authenticated:
    return redirect("/")
  else:
    if request.method=='POST':
      name=request.POST.get('username')
      pwd=request.POST.get('password')
      user=authenticate(request,username=name,password=pwd)
      if user is not None:
        login(request,user)
        messages.success(request,"Log In")
        return redirect("/")
      else:
        messages.error(request,"Invalid User Name or Password")
        return redirect("/login")
    return render(request,"shop/login.html")
 
def register(request):
  form=CustomUserForm()
  if request.method=='POST':
    form=CustomUserForm(request.POST)
    if form.is_valid():
      form.save()
      messages.success(request,"Registration Success You can Login Now..!")
      return redirect('/login')
  return render(request,"shop/register.html",{'form':form})
 
 
def collections(request):
  catagory=Catagory.objects.filter(status=0)
  return render(request,"shop/collections.html",{"catagory":catagory})
 
def collectionsview(request,name):
  if(Catagory.objects.filter(name=name,status=0)):
      products=Product.objects.filter(category__name=name)
      return render(request,"shop/products/index.html",{"products":products,"category_name":name})
  else:
    messages.warning(request,"No Such Catagory Found")
    return redirect('collections')
 
 
def product_details(request,cname,pname):
    if(Catagory.objects.filter(name=cname,status=0)):
      if(Product.objects.filter(name=pname,status=0)):
        products=Product.objects.filter(name=pname,status=0).first()
        return render(request,"shop/products/product_details.html",{"products":products})
      else:
        messages.error(request,"No Such Produtct Found")
        return redirect('collections')
    else:
      messages.error(request,"No Such Catagory Found")
      return redirect('collections')

@login_required
def edit_profile(request):
    if request.method == 'POST':
        username_form = EditProfileForm(request.POST, instance=request.user)
        email_form = EmailChangeForm(request.POST, instance=request.user)
        password_form = ChangePasswordForm(request.user, request.POST)
        
        if username_form.is_valid() and email_form.is_valid() and password_form.is_valid():
            username_form.save()
            email_form.save()
            password_form.save()
            return redirect('logout')  # Redirect to the profile page after changes
    else:
        username_form = EditProfileForm(instance=request.user)
        email_form = EmailChangeForm(instance=request.user)
        password_form = ChangePasswordForm(request.user)
    
    return render(request, 'shop/edit_profile.html', {
        'username_form': username_form,
        'email_form': email_form,
        'password_form': password_form
    })

@login_required
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)

    if cart_items.exists():
        if request.method == "POST":
            address = request.POST.get('address')
            phone_number = request.POST.get('phone_number')
            delivery_mode = request.POST.get('delivery_mode')  # Assuming this is a radio button

            total_amount = sum(item.total_cost for item in cart_items)

            order = Order.objects.create(
                user=request.user,
                address=address,
                phone_number=phone_number,
                delivery_mode=delivery_mode,
                total_amount=total_amount
            )

            for cart_item in cart_items:
                OrderedProduct.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.product_qty,
                    item_price=cart_item.product.selling_price,
                    total_price=cart_item.total_cost
                )

            total_price = sum(ordered_product.item_price for ordered_product in order.orderedproduct_set.all())

            # Prepare and send order confirmation email
            subject = 'Order Confirmation'
            html_message = render_to_string('shop/email/order_confirmation_email.html', {'order': order,'total_price': total_price})
            plain_message = strip_tags(html_message)

            send_mail(
                subject,
                plain_message,
                'sanjay.thiru.17@gmail.com',  # Replace with your sender email
                [order.user.email],  # Sending to the customer's email associated with the order
                html_message=html_message,
            )

            cart_items.delete()

            return render(request, 'shop/order_confirmation.html', {'order': order})
        else:
            return render(request, "shop/checkout.html", {"cart": cart_items})
    else:
        # Redirect or display a message indicating that the cart is empty
        return redirect('cart')  # Redirect to the cart page or display a message
    
def about_us(request):
  return render(request, 'shop/aboutus.html')

def faq(request):
  return render(request, 'shop/faq.html')
