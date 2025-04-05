from django.shortcuts import render, redirect
from .models import RunningPlace

# Create your views here.

running_places = [
    {
        'id' : 1, 'name' : 'Piedmont Park', 'description' : 'beautiful scenery'
    },
    {
        'id' : 2, 'name' : 'Battery Park', 'description' : 'lots of walking'
    },
]
def index(request):
    search_term = request.GET.get('search')
    if search_term:
        running_places = RunningPlace.objects.filter(name__icontains=search_term)
    else:
        running_places = RunningPlace.objects.all()
    template_data = {}
    template_data['title'] = 'Running Places'
    template_data['running_places'] = RunningPlace.objects.all()
    return render(request, 'running_places/index.html', {'template_data': template_data})

def show(request):
    runningPlace = RunningPlace.objects.get(id=id)
    template_data = {}
    template_data['title'] = runningPlace.name
    template_data['runningPlace'] = runningPlace
    return render(request, 'running_places/show.html',
                  {'template_data': template_data})

def create_running_place(request):
    template_data = {}
    template_data['title'] = 'Add Place'
    if request.method == 'POST' and request.POST['name'] != '':
        running_place = RunningPlace()
        running_place.name = request.POST['name']
        running_place.description = request.POST['description']
        running_place.save()
        return redirect('running_places.show')
    else:
        return redirect('running_places.show')