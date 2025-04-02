from django.shortcuts import render

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
    template_data = {}
    template_data['title'] = 'Running Places'
    template_data['running_places'] = running_places
    return render(request, 'running_places/index.html', {'template_data': template_data})

def add_place(request):
    template_data = {}
    template_data['title'] = 'Add Place'
    return render(request, 'running_places/add_place.html', {'template_data': template_data})

def show(request, id):
    running_place = running_places[id - 1]
    template_data = {}
    template_data['title'] = running_place['name']
    template_data['running_place'] = running_place
    return render(request, 'running_places/show.html',
                  {'template_data': template_data})