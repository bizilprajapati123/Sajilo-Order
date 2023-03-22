from django.contrib import auth
from django.contrib import messages
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect,get_object_or_404
from order.models import Order,OrderItem,OrderUpdate
from .forms import RegisterForm, ReportUserForm, UserUpdateform
from .models import MyUser, ReportUser
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import (DjangoUnicodeDecodeError, force_bytes,
                                   force_str)
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from .utils import generate_token
from django.core.paginator import Paginator
from django.urls import reverse
from Trolley.decorators import is_customer

# Create your views here.
# function to send an activation email
def send_activation_email(user, request):
    current_site = get_current_site(request)
    email_subject = "Complete your registration"
    email_body = render_to_string(
        "accounts/activate.html",
        {
            "user": user,
            "domain": current_site.domain,
            "uid": urlsafe_base64_encode(force_bytes(user.id)),
            "token": generate_token.make_token(user),
        },
    )
    email = EmailMessage(subject=email_subject, body=email_body, to=[user.email])

    email.send()
def activate_user(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = MyUser.objects.get(pk=uid)
    except Exception as e:
        user = None
    if user and generate_token.check_token(user, token):
        user.is_active = True
        user.is_email_verified=True
        user.is_profile_verified=True
        user.save()
        messages.success(request, "Email verified, you can now login.")
        return redirect(reverse("accounts:customer_register"))
    else:
        return render(request, "accounts/activate-failed.html", {"user": user})
def customer_register(request):
    if request.user.is_authenticated:
        return redirect('core:home')
    if request.method == 'POST':
        forms = RegisterForm(request.POST)
        if forms.is_valid():
            email=forms.cleaned_data['email']
            password=forms.cleaned_data['password']
            username=forms.cleaned_data['username']
            date_of_birth=forms.cleaned_data['date_of_birth']
            first_name=forms.cleaned_data['first_name']
            last_name=forms.cleaned_data['last_name']
            phone_number=forms.cleaned_data['phone_number']
            user= MyUser(email=email,username=username,date_of_birth=date_of_birth,first_name=first_name,last_name=last_name,phone_number=phone_number)
            user.is_active=False
            user.is_email_verified=False
            user.is_customer=True
            user.is_profile_verified=False
            user.set_password(password)
            user.save()
            send_activation_email(user, request)
            messages.success(
                    request, "Registration Successful, verify your email to login."
            )
        else:
            print(forms.errors)
            context = {
                "error": forms.errors,
            }
            return render(request, 'accounts/customer_register.html', context)
    return render(request, 'accounts/customer_register.html')
def seller_register(request):
    if request.user.is_authenticated:
        return redirect('core:home')
    if request.method == 'POST':
        forms = RegisterForm(request.POST,request.FILES)
        if forms.is_valid():
            print("form is valid")
            email=forms.cleaned_data['email']
            password=forms.cleaned_data['password']
            username=forms.cleaned_data['username']
            date_of_birth=forms.cleaned_data['date_of_birth']
            first_name=forms.cleaned_data['first_name']
            last_name=forms.cleaned_data['last_name']
            phone_number=forms.cleaned_data['phone_number']
            shop_name=forms.cleaned_data['shop_name']
            VatPan_number=forms.cleaned_data['VatPan_number']
            OwnerProof=request.FILES['OwnerProof']
            address=forms.cleaned_data['address']
            user= MyUser(email=email,username=username,date_of_birth=date_of_birth,first_name=first_name,last_name=last_name,phone_number=phone_number,shop_name=shop_name,VatPan_number=VatPan_number,OwnerProof=OwnerProof,address=address)
            user.is_active=False
            user.is_seller=True
            user.set_password(password)
            user.save()
            messages.success(
                    request, "Registration Successful, we will verify your details soon "
            )
        else:
            print(forms.errors)
            context = {
                "errors": forms.errors,
            }
            return render(request, 'accounts/seller_registration.html', context)
    return render(request, 'accounts/seller_registration.html')
def login(request):
    if request.user.is_authenticated:
        return redirect('core:home')
    if request.method == 'POST':
            email = request.POST['email']
            password = request.POST['password']
            user = auth.authenticate(email=email, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('core:home')
            else:
                errors = "User name or password is incorrect"
                return render(request, 'accounts/login.html', {"errors": errors})
    return render(request, 'accounts/login.html')
def logout(request):
    auth.logout(request)
    return redirect('core:home')

@login_required
@is_customer()
def customer_panel(request):
    customers=request.user
    orders=OrderItem.objects.filter(customer=customers)
    paginator = Paginator(orders,8)
    page_number = request.GET.get('page')
    customerord_obj = paginator.get_page(page_number)
    context ={
        'customers':customers,
        'orders':orders,
        'customerord_obj':customerord_obj
    }
    return render(request, 'accounts/customer_panel.html',context)
@login_required
@is_customer()
def customer_edit(request):
    if request.method =='POST':
        form=UserUpdateform(request.POST,instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('accounts:cust-panel')
    else:
        form=UserUpdateform(instance=request.user)      
    context ={
        'form':form
    }
    return render(request,'accounts/customer_panel.html',context)
@login_required
def report_user(request):
    if request.method=='POST':
        form=ReportUserForm(request.POST,request.FILES)
        if form.is_valid():
            proof=request.FILES['proof']
            reason=form.cleaned_data['reason']
            userna=form.cleaned_data['usernames']
            report=ReportUser(proof=proof,reason=reason,usernames=userna)
            report.save()
        else:
            print(form.errors)
        context = {
                "errors": form.errors,
            }
        return render(request, 'accounts/user_reports.html', context)
    return render(request, 'accounts/user_reports.html')
            
@login_required
@is_customer()
def Cancel_order(request,__id):
    data = get_object_or_404(Order,id =__id)
    if request.method == 'POST':
        data.delete()
        OrderUpdate.objects.filter(id=__id).delete()
        return redirect('accounts:cust-panel')
    else:
        return render(request, 'accounts/cancel_ordercustomer.html')