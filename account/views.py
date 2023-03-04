from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from .forms import RegisterUserForm, UserEditForm, PWRestForm
from .token import account_activate_token
from .models import UserBase
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
# Create your views here.


# Register Page 
def register_user(request):
    # if user already login
    if request.user.is_authenticated:
        return redirect('store:home')
    

    if request.method == 'POST':
        
        # collecting information
        register_form = RegisterUserForm(request.POST)
        
        # check the form is valid 
        if register_form.is_valid() :
            user = register_form.save(commit=False)
            user.email = register_form.cleaned_data['email']
            user.set_password(register_form.cleaned_data['password1'])
            user.is_active = False
            user.save()
            
           
            # Setup email
            current_site = get_current_site(request)
            subject = 'Active your account'
            message = render_to_string(
                'account/components/account_activate_email.html',
            {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activate_token.make_token(user)
            })
            user.email_user(subject = subject, message = message )
            return HttpResponse('registered successful and activation sent')

    form = RegisterUserForm()   
    # when method is not post 
    return render(request, 'account/register.html', {'form': form})



def activate_user(request, uidb64, token) -> None:
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = UserBase.objects.get(pk = uid)
        if user and account_activate_token.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return  render(request, 'account/components/activate_valid.html',)
        else:
            return render(request, 'account/components/activate_invalid.html',
                    {
                    'error': 'invalid activate'
                })
    except:
         return render(request, 'account/components/activate_invalid.html',
                    {
                    'error': 'invalid activate'
                })


@login_required(login_url = '/account/login')
def user_dashboard(request):
    return render(request, 'account/user/dashboard.html')



@login_required(login_url='/account/login/')
def profile_edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data = request.POST)
        if user_form.is_valid():
            user_form.save()
    else:
        user_form = UserEditForm(instance = request.user)
    return render(request, 'account/user/edit.html', {'user_form': user_form})
    
@login_required
def delete_user(request):
    user = UserBase.objects.get(username = request.user)
    user.is_active = False
    user.save()
    logout(request)
    return redirect('account:delete-confirmation')
