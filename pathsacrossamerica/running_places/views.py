import os

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import RunningPlace, Review, PATH_TYPE_CHOICES, TERRAIN_TYPE_CHOICES, PARKING_CHOICES, RESTROOM_CHOICES
from dotenv import load_dotenv
import os

#loads.env file
load_dotenv()

#retrieve api key from variable in env file
key = os.getenv("MAPS_API_KEY")
location = "Atlanta, Georgia"
from .utils import validate_address, haversine_distance

# Create your views here.

def index(request):
    template_data = {'title': 'Running Places'}
    search_term = request.GET.get('search')

    if search_term:
        running_places = RunningPlace.objects.filter(name__icontains=search_term)
        template_data['running_places'] = running_places
    else:
        # Only show search bar, no results yet
        template_data['running_places'] = []

    return render(request, 'running_places/index.html', {'template_data': template_data})


@login_required
def create_running_place(request):
    template_data = {'title': 'Add Place'}

    if request.method == 'GET':
        return render(request, 'running_places/add_place.html', {'template_data': template_data})

    if request.method == 'POST':
        name = request.POST.get('name')
        address = request.POST.get('address')

        if not name or not address:
            template_data['error'] = 'Name and address are required.'
            template_data['form_data'] = request.POST
            return render(request, 'running_places/add_place.html', {'template_data': template_data})

        # Step 1: Validate and resolve address using updated function
        lat, lng = validate_address(address)

        if lat is None or lng is None:
            template_data['error'] = 'Invalid or unresolvable address. Please enter a valid one.'
            template_data['form_data'] = request.POST
            return render(request, 'running_places/add_place.html', {'template_data': template_data})

        # Step 2: Save to DB
        running_place = RunningPlace()
        running_place.name = name
        running_place.address = address
        running_place.description = request.POST.get('description', '')
        running_place.path_type = request.POST.get('path_type')
        running_place.terrain_type = request.POST.get('terrain_type')
        running_place.length = request.POST.get('length')
        running_place.parking = request.POST.get('parking')
        running_place.restroom = request.POST.get('restroom')
        running_place.latitude = lat
        running_place.longitude = lng
        running_place.save()

        return redirect('home.index')

    return render(request, 'running_places/add_place.html', {'template_data': template_data})


def show(request, id):
    place = get_object_or_404(RunningPlace, id=id)
    reviews = Review.objects.filter(running_place=place)

    template_data = {}
    template_data['title'] = place.name
    template_data['running_place'] = place
    template_data['reviews'] = reviews

    context = {
        "path_display": PATH_TYPE_CHOICES.get(place.path_type),
        "terrain_display": TERRAIN_TYPE_CHOICES.get(place.terrain_type),
        "parking_display": PARKING_CHOICES.get(place.parking),
        "restroom_display": RESTROOM_CHOICES.get(place.restroom),
    }

    return render(request, 'running_places/show.html', {
        'template_data': template_data, 'context': context
    })

@login_required
def create_review(request, id):
    if request.method == 'POST' and request.POST['comment'] != '':
        running_place = RunningPlace.objects.get(id=id)
        review = Review()
        review.comment = request.POST['comment']
        review.running_place = running_place
        review.user = request.user
        review.save()
        return redirect('running_places.show', id=id)
    else:
        return redirect('running_places.show', id=id)


@login_required
def edit_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.user != review.user:
        return redirect('running_places.show', id=id)
    if request.method == 'GET':
        template_data = {}
        template_data['title'] = 'Edit Review'
        template_data['review'] = review
        return render(request, 'running_places/edit_review.html',
            {'template_data': template_data})
    elif request.method == 'POST' and request.POST['comment'] != '':
        review = Review.objects.get(id=review_id)
        review.comment = request.POST['comment']
        review.save()
        return redirect('running_places.show', id=id)
    else:
        return redirect('running_places.show', id=id)


@login_required
def delete_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id,
        user=request.user)
    review.delete()
    return redirect('running_places.show', id=id)

def get_maps_key():
    return JsonResponse({ 'key': os.environ['MAPS_API_KEY'] })

def find_closest_places(request):
    address = request.GET.get('address')
    path_type = request.GET.get('path_type')
    terrain_type = request.GET.get('terrain_type')
    length = request.GET.get('length')
    parking = request.GET.get('parking')
    restroom = request.GET.get('restroom')

    if not address:
        return render(request, 'index.html', {"message": "Please enter a location"})

    # Use validate_address instead of geocode_address
    user_lat, user_lng = validate_address(address)

    if user_lat is None or user_lng is None:
        return render(request, 'index.html', {"message": f"Could not find the location '{address}'. Please try again."})


    places = RunningPlace.objects.all()
    if path_type != "":
        places = places.filter(path_type=path_type)
    if terrain_type != "":
        places = places.filter(terrain_type=terrain_type)
    if length:
        places = places.filter(length__lte=length)
    if parking != "":
        places = places.filter(parking=parking)
    if restroom != "":
        places = places.filter(restroom=restroom)
    place_distances = []

    for place in places:
        dist = haversine_distance(
            float(user_lat), float(user_lng),
            float(place.latitude), float(place.longitude)
        )
        place_distances.append((dist, place))

    place_distances.sort(key=lambda x: x[0])
    top_3 = place_distances[:3]

    results = [
        {
            'distance': d,
            'place': p,
            'lat': float(p.latitude),
            'lng': float(p.longitude),
            'directions_url': f"https://www.google.com/maps/dir/?api=1&origin={user_lat},{user_lng}&destination={p.latitude},{p.longitude}&travelmode=driving"
        } for (d, p) in top_3
    ]

    markers_str = ""
    for i, r in enumerate(results, start=1):
        markers_str += f"&markers=color:red%7Clabel:{i}%7C{r['lat']},{r['lng']}"

    key = os.getenv("MAPS_API_KEY")
    #center = f"{user_lat},{user_lng}"
    # Use visible to auto-zoom the map to include all points
    visible_bounds = "|".join([f"{r['lat']},{r['lng']}" for r in results])

    static_map_url = (
        "https://maps.googleapis.com/maps/api/staticmap"
        f"?size=600x400"
        f"{markers_str}"
        f"&visible={visible_bounds}"
        f"&key={key}"
    )

    context = {
        'address': address,
        'user_lat': user_lat,
        'user_lng': user_lng,
        'static_map_url': static_map_url,
        'results': results
    }

    return render(request, 'running_places/places_list.html', context)
