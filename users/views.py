from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from .models import advertisement
from django.core.files.storage import FileSystemStorage
import os



def register(request):
    
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! Please login.')
            form.save()
            return redirect('login')
        
    else:
        form = UserRegisterForm()
    
    return render(request, 'users/register.html', {'form':form})


@login_required
def profile(request):
    
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Account successfully updated.')
            return redirect('profile')
        
    else:
        
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        
    context = {
        'u_form': u_form,
        'p_form': p_form

    }
    
    return render(request, 'users/profile.html', context)

@login_required
def upload(request):
    if request.method == 'POST':
        
        #Validates that the user initiated a POST request
        
        if request.POST.get('name'):
            
            #Checks if the form has a name value
            
            newPath = r'C:\Users\DrapelickClient2\AppData\Local\Programs\Python\Python38-32\Scripts\django_project\media\AdDirectory'\
        + str(request.user)
            newPath.replace(' ', '')
            if not os.path.exists(newPath):
                 
                #This part makes a new file directory to hold the ads, if none already exist.
                os.makedirs(newPath)
                
                
            #These two parts (fs and ad) saves the ad image file and adds the form data to
            #the database
            
            uploaded_file = request.FILES['adImage']
            fs = FileSystemStorage()
            name = fs.save(uploaded_file.name, uploaded_file)
            url = fs.url(name)
            print("ok")
            #print(url)
            

            ad = advertisement()
            ad.location = url
            ad.name = request.POST.get('name')
            ad.user = request.user.username
            ad.save()

            messages.success(request, f'{ad.name} successfully uploaded.')
            
            return render(request, 'users/upload.html')

    else:
        return render(request, 'users/upload.html')

@login_required
def gallery(request):
    context = {'ads':advertisement.objects.all()}
    return render(request, 'users/gallery.html', context)
