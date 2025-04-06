from django.shortcuts import render

# Create your views here.
def index(request):
    template_data = {}
    template_data['title'] = 'Paths Across America'
    return render(request, 'home/index.html', {'template_data': template_data})