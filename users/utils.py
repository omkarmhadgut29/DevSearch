from .models import Profile, Skill
from django.db.models import Q

# Searching developers by name, skills, description, etc.
def searchProfiles(request):

    search_query = ""

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
    
    skill = Skill.objects.filter(Q(name__icontains=search_query))

    profiles = Profile.objects.distinct().filter(
        Q(name__icontains=search_query) | 
        Q(short_intro__icontains=search_query) |
        Q(skill__in=skill)
        )
    
    return profiles, search_query
