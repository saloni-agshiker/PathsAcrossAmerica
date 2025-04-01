from django.shortcuts import render

# Create your views here.
def add_place(request):
    template_data = {}
    template_data['title'] = 'Add Place'
    return render(request, 'running_places/add_place.html', {'template_data': template_data})
