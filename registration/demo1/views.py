from django.contrib.auth.models import User
from .models import Profile,Product,Cart
from django.shortcuts import render,redirect
import random
import requests
from django.db.models import Count, Q
from django.views import View
from django.http import JsonResponse


def send_otp(numb,otp):
    try:
        num1 = str(numb)
        url = 'https://2factor.in/API/V1/e474594b-dba6-11ed-addf-0200cd936042/SMS/' + num1 + '/' + otp
        requests.get(url)
    except Exception as e:
        return None


# Create your views here.
def homePage(request):
    return render(request,'home.html')


def signupPage(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        numb = request.POST.get('num')
        mail = request.POST.get('mail')
        otp = str(random.randint(1000,9999))
        print (name,numb,mail)
        user = User.objects.create_user(name,mail,numb)
        user.save()
        profile = Profile(user = user,mobile = numb,otp = otp)
        profile.save()
        send_otp(numb,otp)
        request.session[ 'numb' ] = numb
        return redirect('otp')
    return render(request,'login1page.html')


def loginPage(request):
    numb = request.session[ 'numb' ]
    if request.method == 'POST':
        otp = request.POST.get('otp')
        profile = Profile.objects.filter(mobile = numb).first()
        if otp == profile.otp:
            return redirect('home')
        else:
            comtext = {'message': 'Wrong OTP','class': 'danger','numb': numb}
            return render(request,'passotp.html',comtext)
    return render(request,'passotp.html')


class CategoryView(View):
    def get(self,request,val):
        product = Product.objects.filter(category = val)
        title = Product.objects.filter(category = val).values('title').annotate(total = Count('title'))
        return render(request,"category.html",locals())


class ProductDetail(View):
    def get(self,request,pk):
        product = Product.objects.filter(pk = pk)
        return render(request,"productdetail.html",locals())


def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')

    product = Product.objects.get(id = product_id)
    Cart(user = user,product = product).save()
    return redirect("/cart")


def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user = user)
    amount =0
    for p in cart:
        value = p.quantity* p.product.discounted_price
        amount = amount + value
    totalamount = amount * 1.25
    return render(request,'addtocart.html',locals())


def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c= Cart.objects.get(Q(product = prod_id)&Q(user= request.user))
        c.quantity+=1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount * 1.25
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }

        return JsonResponse(data)


def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c= Cart.objects.get(Q(product = prod_id)&Q(user= request.user))
        c.quantity -= 1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount * 1.25
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }

        return JsonResponse(data)


def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product = prod_id) & Q(user= request.user))
        c.quantity = 0
        c.delete()
        user = request.user
        cart = Cart.objects.filter(user = user)
        amount = 0
        for p in cart :
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount * 1.25
        data={
            'amount':amount,
            'totalamount':totalamount
        }

        return JsonResponse(data)


class checkout(View):
    def get(self,request):
        user = request.user

        cart_items = Cart.objects.filter(user= user)
        famount=0
        for p in cart_items:
            value = p.quantity * p.product.discounted_price
            famount = famount + value
        totalamount= famount*1.25



        return render(request,'checkout.html',locals())


def search(request):
    query = request.GET['search']
    totalitem = 0

    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user = request.user))

    product = Product.objects.filter(Q(title__icontains = query))
    return render(request,"search.html",locals())

def prints(request):
    print("hello")
    return render(request,'home.html')
