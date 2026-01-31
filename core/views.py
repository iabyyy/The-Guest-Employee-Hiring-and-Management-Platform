from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


from .models import (
    ContractorProfile,
    GuestEmployeeProfile,
    Job,
    Feedback
)

from django.shortcuts import render

def home(request):
    return render(request, 'home.html')



# Register Page
# URL: /register/
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        role = request.POST['role']

        user = User.objects.create_user(username=username, password=password)

        if role == 'contractor':
            ContractorProfile.objects.create(
                user=user,
                company_name='Default Company',
                requirements='Not specified'
            )
        else:
            GuestEmployeeProfile.objects.create(
                user=user,
                skills='Not specified',
                experience=0,
                availability='Available'
            )

        return redirect('login')

    return render(request, 'register.html')


# Login Page
# URL: /login/
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .models import ContractorProfile, GuestEmployeeProfile

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            try:
                ContractorProfile.objects.get(user=user)
                return redirect('contractor')
            except ContractorProfile.DoesNotExist:
                pass

            try:
                GuestEmployeeProfile.objects.get(user=user)
                return redirect('guest')
            except GuestEmployeeProfile.DoesNotExist:
                pass

            return redirect('home')

    return render(request, 'login.html')


# Contractor Dashboard
# URL: /contractor/
def contractor_dashboard(request):
    jobs = Job.objects.filter(contractor__user=request.user)
    return render(
        request,
        'contractor_dashboard.html',
        {'jobs': jobs}
    )


# Guest Dashboard
# URL: /guest/
def guest_dashboard(request):
    return render(request, 'guest_dashboard.html')


# Post Job Page
# URL: /post-job/
def post_job(request):
    if request.method == 'POST':
        contractor = ContractorProfile.objects.get(user=request.user)

        Job.objects.create(
            contractor=contractor,
            title=request.POST['title'],
            description=request.POST['description'],
            required_skills=request.POST['skills']
        )

        return redirect('contractor')

    return render(request, 'post_job.html')


# Search Guest Page
# URL: /search-guest/
def search_guest(request):
    guests = GuestEmployeeProfile.objects.all()
    return render(
        request,
        'search_guest.html',
        {'guests': guests}
    )


# Feedback Page
# URL: /feedback/
def feedback(request):
    if request.method == 'POST':
        Feedback.objects.create(
            from_user=request.user,
            to_user=User.objects.get(username=request.POST['to_user']),
            rating=request.POST['rating'],
            comment=request.POST['comment']
        )

        return redirect('home')

    return render(request, 'feedback.html')



@login_required
def contractor_dashboard(request):
    jobs = Job.objects.filter(contractor__user=request.user)
    return render(request, 'contractor_dashboard.html', {'jobs': jobs})


@login_required
def guest_dashboard(request):
    return render(request, 'guest_dashboard.html')


from django.contrib.auth import logout

def user_logout(request):
    logout(request)
    return redirect('login')
