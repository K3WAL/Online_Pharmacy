import json
import pprint
import base64
import requests
import decimal
import numpy as np
import pytesseract
import pytesseract as tess
from PIL import Image
from urllib import request 
from re import search
from platformdirs import user_cache_dir
from requests import delete
from matplotlib.pyplot import title
from unicodedata import category
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.views import View
from django.core.paginator import Paginator
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.db.models import Q 
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import CustomerRegistrationForm, CustomerProfileForm
from .models import *



#install tesseract module from here - https://github.com/UB-Mannheim/tesseract/wiki
pytesseract.pytesseract.tesseract_cmd = (
    r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Path to tesseract.exe
)


class ProductView(View):
    def get(self, request):
        totalitem = 0
        covid_essentials = Product.objects.filter(category='CE')
        family_cares = Product.objects.filter(category='FC')
        personal_cares = Product.objects.filter(category='PC')
        ayurvedics = Product.objects.filter(category='A')
        surgicals = Product.objects.filter(category='S')
        devices = Product.objects.filter(category='D')
        immunity_boosters = Product.objects.filter(category='IB')
        sexual_wellness= Product.objects.filter(category='SW')
        medicines = Product.objects.filter(category='M')
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request, 'app/index.html', 
        {'covid_essentials':covid_essentials, 'family_cares':family_cares, 'personal_cares':personal_cares, 
        'ayurvedics':ayurvedics, 'surgicals':surgicals, 'devices ':devices , 
        'immunity_boosters':immunity_boosters,'sexual_wellness':sexual_wellness, 'medicines':medicines, 'totalitem':totalitem})


class ProductDetailView(View):
    def get(self, request, pk):
        totalitem = 0
        product = Product.objects.get(pk=pk)
        item_already_in_cart = False
        related_products = Product.objects.filter(category=product.category).exclude(pk=pk)[:4]
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
        return render(request, 'app/productdetail.html', {'product':product, 'item_already_in_cart':item_already_in_cart,
         'totalitem':totalitem, 'related_products':related_products})

def family(request):
    totalitem = 0
    family_cares = Product.objects.filter(category='FC')
    paginator = Paginator(family_cares, 8)
    page_number = request.GET.get('page')
    family = paginator.get_page(page_number)
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/collections/family.html', {'family':family, 'totalitem':totalitem})

def covid(request):
    totalitem = 0
    covid_essential = Product.objects.filter(category='CE')
    paginator = Paginator(covid_essential, 8)
    page_number = request.GET.get('page')
    covid = paginator.get_page(page_number)
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/collections/covid.html', {'covid':covid, 'totalitem':totalitem})


def personal(request):
    totalitem = 0
    personal_cares = Product.objects.filter(category='PC')
    paginator = Paginator(personal_cares, 8)
    page_number = request.GET.get('page')
    personal = paginator.get_page(page_number)
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/collections/personal.html', {'personal':personal, 'totalitem':totalitem})

def ayurvedic(request):
    totalitem = 0
    ayurvedics = Product.objects.filter(category='A')
    paginator = Paginator(ayurvedics, 8)
    page_number = request.GET.get('page')
    ayurvedics = paginator.get_page(page_number)
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/collections/ayurvedic.html', {'ayurvedics':ayurvedics, 'totalitem':totalitem})

def surgical(request):
    totalitem = 0
    surgicals = Product.objects.filter(category='S')
    paginator = Paginator(surgicals, 8)
    page_number = request.GET.get('page')
    surgicals = paginator.get_page(page_number)
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/collections/surgical.html', {'surgicals':surgicals, 'totalitem':totalitem})

def devices(request):
    totalitem = 0
    devices = Product.objects.filter(category='D')
    paginator = Paginator(devices, 8)
    page_number = request.GET.get('page')
    devices = paginator.get_page(page_number)
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/collections/devices.html', {'devices':devices, 'totalitem':totalitem})

def immunity(request):
    totalitem = 0
    immunity_boosters = Product.objects.filter(category='IB')
    paginator = Paginator(immunity_boosters, 8)
    page_number = request.GET.get('page')
    immunity = paginator.get_page(page_number)
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/collections/immunity.html', {'immunity':immunity, 'totalitem':totalitem})

def wellness(request):
    totalitem = 0
    sexual_wellness= Product.objects.filter(category='SW')
    paginator = Paginator(sexual_wellness, 8)
    page_number = request.GET.get('page')
    wellness = paginator.get_page(page_number)
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/collections/wellness.html', {'wellness':wellness, 'totalitem':totalitem})

def medicine(request):
    totalitem = 0
    medicines = Product.objects.filter(category='M')
    paginator = Paginator(medicines, 8)
    page_number = request.GET.get('page')
    medicines = paginator.get_page(page_number)
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/collections/medicine.html', {'medicines':medicines, 'totalitem':totalitem})

@login_required
def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html', {'add':add, 'active':'btn-primary'})


class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html', {'form':form})

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Congurations!! Registered Successfully')
            form.save()
        return render(request, 'app/customerregistration.html', {'form':form})

def password_reset(request):
 return render(request, 'app/password_reset.html')
 
def passwordchangedone(request):
 return render(request, 'app/password_reset.html')


@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        return render(request, 'app/profile.html', {'form':form, 'active':'btn-primary'})

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality'] 
            city = form.cleaned_data['city']
            area = form.cleaned_data['area']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=usr, name=name, locality=locality, city=city, area=area, zipcode=zipcode)
            reg.save()
            messages.success(request, 'Congurations!! Profile Updated Successully')
        return render(request, 'app/profile.html', {'form':form, 'active':'btn-primary'})

@login_required
def buynow(request):
    user=request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect('/checkout/')

def add_to_cart(request):
    user=request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect('/cart/')

@login_required
def show_cart(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = decimal.Decimal(0.0)
        shipping_amount = decimal.Decimal(50.00)
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.selling_price)
                amount += tempamount
                totalamount = amount + shipping_amount
            return render(request, 'app/addtocart.html', {'carts':cart, 'totalamount':totalamount, 'amount':amount, 'totalitem':totalitem})
        else:
            return render(request, 'app/emptycart.html')

def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        amount = decimal.Decimal(0.0)
        shipping_amount = decimal.Decimal(50.00)
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.selling_price)
            amount += tempamount

            data = {
                'quantity': c.quantity,
                'amount':amount,
                'totalamount':amount + shipping_amount
            }
        return JsonResponse(data)


def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        amount = decimal.Decimal(0.0)
        shipping_amount = decimal.Decimal(50.00)
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.selling_price)
            amount += tempamount
        
            data = {
                'quantity': c.quantity,
                'amount':amount,
                'totalamount':amount + shipping_amount
            }
        return JsonResponse(data)

def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount = decimal.Decimal(0.0)
        shipping_amount = decimal.Decimal(50.00)
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        data = {
            "amount": 0
        }
        for p in cart_product:
            tempamount = (p.quantity * p.product.selling_price)
            amount += tempamount

            data = {
                'amount':amount,
                'totalamount':amount + shipping_amount
            }
        return JsonResponse(data)

@login_required
def checkout(request):
    totalitem = 0
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_item = Cart.objects.filter(user=user)
    amount = decimal.Decimal(0.0)
    shipping_amount = decimal.Decimal(50.00)
    totalamount = decimal.Decimal(0.0)
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    if cart_product:
        for p in cart_product:
            tempamount = (p.quantity * p.product.selling_price)
            amount += tempamount
        totalamount = amount + shipping_amount
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/checkout.html', {'add':add, 'totalamount':totalamount, 'cart_item':cart_item, 'totalitem':totalitem})

@login_required
def payment_done(request):
    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id=custid)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity).save()
        c.delete()
    return redirect("orders")

@login_required
def orders(request):
    op = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html', {'order_placed':op})

class SearchView(TemplateView):
    template_name = "app/search.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        kw = self.request.GET.get("keyword", "")
        results = Product.objects.filter(Q(title__icontains=kw) | Q(description__icontains=kw))
        paginator = Paginator(results, 10)
        request = self.request
        page_number = request.GET.get('page')
        results = paginator.get_page(page_number)
        context["results"] = results 
        return context


def contact(request):
    if request.method=="POST":
        name = request.POST['name']
        subject = request.POST['subject']
        email = request.POST['email']
        content = request.POST['content']
        if len(name)<2 or len(email)<5 or len(subject)<5 or len(content)<5:
            messages.error(request, "Please fill the form correctly")
        else:
            contact = Contact(name=name, subject=subject, email=email, content=content)
            contact.save()
            messages.success(request, "Your Message has been Successfully Sent")
    return render(request, 'app/contact.html')

def about(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/about.html', {'totalitem':totalitem})

def index(request):
    totalitem = 0
    ayurvedics = Product.objects.filter(category='A')
    paginator = Paginator(ayurvedics, 8)
    page_number = request.GET.get('page')
    ayurvedics = paginator.get_page(page_number)
    personal_cares = Product.objects.filter(category='PC')
    devices = Product.objects.filter(category='D')
    if request.user.is_authenticated:  
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/home.html', {'totalitem':totalitem, 'ayurvedics': ayurvedics, 'personal_cares':personal_cares, 'devices':devices})

def verify_payment(request):
   data = request.POST
   product_id = data['product']
   token = data['token']
   amount = data['totalamount']

   url = "https://khalti.com/api/v2/payment/verify/"
   payload = {
   "token": token,
   "amount": amount
   }
   headers = {
   "Authorization": "test_secret_key_32f0ddab652a4386a3684da6de0fcdc9"
   }
   response = requests.post(url, payload, headers = headers)
   
   response_data = json.loads(response.text)
   status_code = str(response.status_code)

   if status_code == '400':
      response = JsonResponse({'status':'false','message':response_data['detail']}, status=500)
      return response

   import pprint 
   pp = pprint.PrettyPrinter(indent=4)
   pp.pprint(response_data)
   
   return JsonResponse(f"Payment Done !! With IDX. {response_data['user']['idx']}",safe=False)



def prescription(request):
    if request.method == "POST":
        try:
            image = request.FILES["imagefile"]
            # encode image to base64 string
            image_base64 = base64.b64encode(image.read()).decode("utf-8")
        except:
            messages.add_message(
                request, messages.ERROR, "No image selected or uploaded"
            )
            return render(request, "app/prescription.html")
        img = np.array(Image.open(image))
        text = pytesseract.image_to_string(img)
        arr = text.split()
        results = Product.objects.filter(title__icontains=arr[0])
        # return text to html
        return render(request, "app/prescription.html", {"results": results, "text":text})
    return render(request, "app/prescription.html")


def newsletter(request):
    if request.method=="POST":
        email = request.POST['email']
        if len(email)<4:
            messages.error(request, "Provide email correctly")
        else:
            contact = Newsletter(email=email)
            contact.save()
            messages.success(request, "email updated")
    return render(request, 'app/index.html')