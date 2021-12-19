from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import redirect, render
from .models import Project, Tag
from .project_forms import ProjectForm
from .utils import searchProjects


def projects(request):
    projects, search_query = searchProjects(request)

    page = request.GET.get('page')
    result = 3
    paginator = Paginator(projects, result)

    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        projects = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        projects = paginator.page(page)

    context = {
        'projects': projects, 
        'search_query': search_query,
        'paginator': paginator,
    }
    return render(request, './projects/project.html', context)

def project(request, pk):
    projectObj = Project.objects.get(id=pk)
    tags = Tag.objects.all()
    return render(request, './projects/single-project.html', {'project': projectObj, 'tags': tags})

@login_required(login_url='Login')
def create_project(request):
    profile = request.user.profile
    form = ProjectForm()

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(commit=False).owner = profile
            form.save()
            return redirect("account")

    context = {'form': form}
    return render(request, './projects/project_form.html', context)


@login_required(login_url='Login')
def updateProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    form = ProjectForm(instance=project)

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect("account")

    context = {'form': form}
    return render(request, './projects/project_form.html', context)


@login_required(login_url='Login')
def deleteProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)

    if request.method == "POST":
        project.delete()
        return redirect("account")

    context = {'object': project}
    return render(request, "./delete_template.html", context)