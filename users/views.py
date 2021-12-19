from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CostomUserCreationForm, ProfileForm, SkillForm
from django.db.models import Q
from django.contrib.auth.models import User
from .models import Profile
from .utils import searchProfiles

# Login page for user
def loginPage(request):
    page = "login"
    context = {'page': page}

    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Username does not exist')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('projects')
        else:
            messages.error(request, 'Username or password is incorrect')

    return render(request, 'users/login_register.html', context)


# Logout page for user
def logoutPage(request):
    logout(request)
    messages.info(request, 'Logged out successfully')
    return redirect('Login')

def registerUser(request):
    page = "register"
    form = CostomUserCreationForm()

    if request.method == 'POST':
        form = CostomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, 'User created successfully')
            login(request, user)
            return redirect('edit-account')
        else:
            messages.error(request, 'User creation failed')


    context = {'page': page, 'form': form}
    return render(request, 'users/login_register.html', context)

def profiles(request):
    
    profile, search_query = searchProfiles(request)

    context = {'profiles': profile, 'search_query': search_query}
    return render(request, 'users/profiles.html', context)

def userProfile(request, pk):
    profiles = Profile.objects.get(id=pk)

    topSkills = profiles.skill_set.exclude(description__exact="")
    otherSkills = profiles.skill_set.filter(description="")

    context = {'profile': profiles, "topSkills": topSkills, "otherSkills": otherSkills}
    return render(request, 'users/user-profile.html', context)

@login_required(login_url='Login')
def userAccount(request):
    profile = request.user.profile
    skills = profile.skill_set.all()
    projects = profile.project_set.all()
    context = {"profile": profile, "skills": skills, "projects": projects}
    return render(request, 'users/account.html', context)

@login_required(login_url='Login')
def editAcoount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('account')
        else:
            messages.error(request, 'Profile update failed')

    context = {"form": form}
    return render(request, 'users/profile_form.html', context)


# create skill
@login_required(login_url='Login')
def createSkill(request):
    profile = request.user.profile
    form = SkillForm()
    
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request, 'Skill created successfully')
            return redirect('account')
        else:
            messages.error(request, 'Skill creation failed')

    return render(request, 'users/skill_form.html', {"form": form})

# Update skill
@login_required(login_url='Login')
def updateSkill(request, pk):
    profile = request.user.profile
    skills = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skills)
    
    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skills)
        if form.is_valid():
            form.save()
            messages.success(request, 'Skill updated successfully')
            return redirect('account')
        else:
            messages.error(request, 'Skill updation failed')

    return render(request, 'users/skill_form.html', {"form": form})


# Delete Skills
def deleteSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)

    if request.method == 'POST':
        skill.delete()
        messages.success(request, 'Skill deleted successfully')
        return redirect('account')

    context = {"object": skill}
    return render(request, 'delete_template.html', context)

