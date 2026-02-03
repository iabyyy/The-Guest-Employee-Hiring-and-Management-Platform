from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import (
    ContractorProfile,
    GuestEmployeeProfile,
    Job,
    Feedback
)


# =======================
# HOME
# =======================
def home(request):
    return render(request, 'home.html')


# =======================
# REGISTER
# =======================
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('register')

        user = User.objects.create_user(
            username=username,
            password=password
        )

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

        messages.success(request, 'Registration successful. Please login.')
        return redirect('login')

    return render(request, 'register.html')


# =======================
# LOGIN
# =======================
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect based on profile type
            if hasattr(user, 'contractorprofile'):
                return redirect('contractor')
            elif hasattr(user, 'guestemployeeprofile'):
                return redirect('guest')
            else:
                messages.error(request, 'Profile not found.')
                return redirect('home')
        messages.error(request, 'Invalid username or password')
    return render(request, 'login.html')



# =======================
# LOGOUT
# =======================
def user_logout(request):
    logout(request)
    return redirect('login')


# =======================
# CONTRACTOR DASHBOARD
# =======================
@login_required
def contractor_dashboard(request):
    jobs = Job.objects.filter(contractor__user=request.user)
    return render(
        request,
        'contractor_dashboard.html',
        {'jobs': jobs}
    )


# =======================
# GUEST DASHBOARD
# =======================
@login_required
def guest_dashboard(request):
    return render(request, 'guest_dashboard.html')


# =======================
# POST JOB
# =======================
@login_required
def post_job(request):
    contractor = ContractorProfile.objects.get(user=request.user)

    if request.method == 'POST':
        Job.objects.create(
            contractor=contractor,
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            required_skills=request.POST.get('skills')
        )
        messages.success(request, 'Job posted successfully')
        return redirect('contractor')

    return render(request, 'post_job.html')


# =======================
# SEARCH GUEST
# =======================
@login_required
def search_guest(request):
    guests = GuestEmployeeProfile.objects.all()
    return render(
        request,
        'search_guest.html',
        {'guests': guests}
    )


# =======================
# FEEDBACK
# =======================
@login_required
def feedback(request):
    if request.method == 'POST':
        to_username = request.POST.get('to_user')
        try:
            to_user = User.objects.get(username=to_username)

            # Create the feedback
            Feedback.objects.create(
                from_user=request.user,
                to_user=to_user,
                rating=request.POST.get('rating'),
                comment=request.POST.get('comment')
            )

            messages.success(request, 'Feedback submitted')

            # Redirect to the dashboard of the user who received feedback
            if hasattr(to_user, 'contractorprofile'):
                return redirect('contractor')
            elif hasattr(to_user, 'guestemployeeprofile'):
                return redirect('guest')
            else:
                # fallback
                return redirect('home')

        except User.DoesNotExist:
            messages.error(request, 'User not found')
            return redirect('feedback')

    return render(request, 'feedback.html')