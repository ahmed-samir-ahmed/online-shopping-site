from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .models import UserProfile
import re
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib import auth
from django.contrib.auth.forms import PasswordChangeForm
from products.models import Product
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required


def signin(request):
    if request.method == 'POST'and 'btnlogin' in request.POST:

       username = request.POST['user']
       password = request.POST['pass']
       user = auth.authenticate(username=username,password=password)
       if user is not None:
           if 'rememberme' not in request.POST:
               request.session.set_expiry(0)
           auth.login(request,user)
           #messages.success(request,'you are login correctly')
           return redirect('signin')
       else:
           messages.error(request, 'username or password is incorrect')
           return render(request, 'accounts/signin.html')



    else:
        return render (request, 'accounts/signin.html')



def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
    return redirect('index')


def signup(request):
    if request.method == 'POST' and 'btnsignup' in request.POST:

        fname = None
        lname = None
        address = None
        address2 = None
        zip_number = None
        state = None
        city = None
        username = None
        email = None
        password = None
        terms = None
        is_added = None

        if 'fname' in request.POST: fname = request.POST['fname']
        else: messages.error(request, 'Error in first_name')

        if 'lname' in request.POST: lname = request.POST['lname']
        else: messages.error(request, 'Error in last_name')

        if 'address' in request.POST: address = request.POST['address']
        else: messages.error(request, 'Error in address')

        if 'address2' in request.POST: address2 = request.POST['fname']
        else:  messages.error(request, 'Error in address2')

        if 'city' in request.POST: city = request.POST['city']
        else: messages.error(request, 'Error in city')

        if 'state' in request.POST: state = request.POST['state']
        else: messages.error(request, 'Error in state')

        if 'zip' in request.POST: zip_number = request.POST['zip']
        else: messages.error(request, 'Error in zip')

        if 'email' in request.POST: email = request.POST['email']
        else: messages.error(request, 'Error in email')

        if 'user' in request.POST: username = request.POST['user']
        else: messages.error(request, 'Error in user_name')

        if 'pass' in request.POST: password = request.POST['pass']
        else: messages.error(request, 'Error in password')
        
        if 'terms' in request.POST: terms = request.POST['terms']

        if fname and lname and city and address and address2 and zip_number and email and state and username and password:
            if terms == 'on':
                if User.objects.filter(username=username).exists():
                    messages.error(request,'username is taken')
                else:
                    if User.objects.filter(email=email).exists():
                        messages.error(request, 'This email is token')
                    else:
                        patt = "^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+$"
                        if re.match(patt,email):


                            user = User.objects.create_user(first_name=fname,last_name=lname, email=email,username=username,password=password)
                            user.save()
                            userprofile=UserProfile(user=user,address=address,address2=address2,zip_number=zip_number,state=state,city=city)
                            userprofile.save()
                            # clean all fields

                            fname=''
                            lname=''
                            address=''
                            address2=''
                            city=''
                            state=''
                            zip_number=''
                            email=''
                            username=''
                            password=''
                            terms=None



                            #success registreation
                            messages.success(request, 'Your Account is Created')
                            is_added = True
                        else:
                            messages.error(request, 'invalid email')




            else:
                messages.error(request, 'you mast agree our policy')
        else:
            messages.error(request ,'Check The empty filed')













        return render (request, 'accounts/signup.html',{
            'fname':fname,
            'lname':lname,
            'address':address,
            'address2':address2,
            'state':state,
            'zip':zip_number,
            'city':city,
            'email':email,
            'usre':username,
            'pass':password,
            'is_added':is_added



        })
    else:
        return render (request, 'accounts/signup.html')




def profile(request):
    if request.method == 'POST'and 'btnsave' in request.POST:
        if request.user is not None and request.user.id !=None:
            userprofile = UserProfile.objects.get(user=request.user)
            if request.POST['fname'] and request.POST['lname'] and request.POST['address'] and  request.POST['address2'] and request.POST['address2'] and request.POST['city'] and  request.POST['state'] and request.POST['zip'] and request.POST['email'] and  request.POST['user'] and request.POST['pass']:
                request.user.first_name = request.POST['fname']
                request.user.last_name = request.POST['lname']
                userprofile.address = request.POST['address']
                userprofile.address2 = request.POST['address2']
                userprofile.city = request.POST['city']
                userprofile.state = request.POST['state']
                userprofile.zip_number = request.POST['zip']
                #request.user.email = request.POST['email']
                #request.user.username = request.POST['user']
                form = PasswordChangeForm(request.user)

                request.user.save()
                userprofile.save()

                messages.success(request, 'your data has been changed correctly')
                return redirect('profile')
            else:
                messages.error(request,'check your value and elemnts')
                return redirect('profile')

        return redirect('profile')
    else:
        if request.user is not None:
            userprofile = UserProfile.objects.get(user=request.user)
            context = {
                    'fname':request.user.first_name,
                    'lname': request.user.last_name,
                    'email': request.user.email,
                    'user':request.user.username,
                    'pass':request.user.password,
                    'address':userprofile.address,
                    'address2':userprofile.address2,
                    'city':userprofile.city,
                    'zip':userprofile.zip_number,
                    'state':userprofile.state,

            }

            return render(request, 'accounts/profile.html',context)
        else:
            return redirect('profile')




def product_favorite(request, pro_id):
    if request.user.is_authenticated and not request.user.is_anonymous:
        pro_fav = Product.objects.get(pk=pro_id)
        if UserProfile.objects.filter(user=request.user,product_favorites=pro_fav).exists:
            messages.info(request, 'The Product hs been in your products_favoraits')
        else:
            userprofile = UserProfile.objects.get(user=request.user)
            userprofile.products_favorites.add(pro_fav)
            messages.success(request,'product has been favorated')
        return redirect('/products/' + str(pro_id))
    else:
        return redirect('index')








def show_product_favorite(request):
    context = None
    if request.user.is_authenticated and not request.user.is_anonymous:
        userInfo = UserProfile.objects.get(user=request.user)
        pro = userInfo.product_favorites.all()
        context = {'products':pro}
    return render(request, 'products/products.html',context)