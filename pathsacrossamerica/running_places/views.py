import os

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import RunningPlace, Review
from .utils import geocode_address, haversine_distance

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

@login_required
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
    return render(request, 'running_places/add_place.html', {'template_data': template_data})

def show(request, id):
    place = get_object_or_404(RunningPlace, pk=id)
    reviews = Review.objects.filter(running_place=place)

    template_data = {}
    template_data['title'] = place.name
    template_data['running_place'] = place
    template_data['reviews'] = reviews

    return render(request, 'running_places/show.html', {
        'template_data': template_data
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

def find_closest_places(request):
    address = request.GET.get('address')

    # if no address, renders a form message
    if not address:
        return render(request, 'index.html', {"message": "Please enter a location"})

    user_lat, user_lng = geocode_address(address)
    if user_lat is None or user_lng is None:
        # geocoding failed or location not found
        return render(request, 'index.html', {"message": f"Could not find the location '{address}'. Please try again."})

        # --- Testing Without Database Records ---
        # If there are no records, simulate dummy data.
    if not RunningPlace.objects.exists():
        # Create dummy results with hardcoded coordinates for testing.
        results = [
            {
                'distance': 0.0,
                'place': type("Dummy", (),
                              {"name": "Test Place 1", "description": "A dummy location", "latitude": 33.7490,
                               "longitude": -84.3880})(),
                'lat': 33.7490,
                'lng': -84.3880,
            },
            {
                'distance': 1.2,
                'place': type("Dummy", (),
                              {"name": "Test Place 2", "description": "Another dummy", "latitude": 33.7580,
                               "longitude": -84.3900})(),
                'lat': 33.7580,
                'lng': -84.3900,
            },
            {
                'distance': 2.5,
                'place': type("Dummy", (),
                              {"name": "Test Place 3", "description": "Yet another dummy", "latitude": 33.7600,
                               "longitude": -84.3950})(),
                'lat': 33.7600,
                'lng': -84.3950,
            },
        ]

    else:
    # queries all places
        places = RunningPlace.objects.all()
        # calculate distance for each place
        place_distances = []
        for place in places:
            dist = haversine_distance(
                float(user_lat), float(user_lng),
                float(place.latitude), float(place.longitude)
            )
            place_distances.append((dist, place))

        #sort (distance, place) pairs
        place_distances.sort(key=lambda x: x[0])

        #slice top 3
        top_3 = place_distances[:3]

        results = [
            {
                'distance' : d,
                'place': p,
                'lat': float(p.latitude),
                'lng': float(p.longitude),
            } for(d,p) in top_3
        ]

    markers_str = ""
    for i, r in enumerate(results, start=1):
        markers_str += f"&markers=color:red%7Clabel:{i}%7C{r['lat']},{r['lng']}"

    key = os.getenv("MAPS_API_KEY")  # Make sure your .env is correctly loaded!
    # Use the user's search coordinates as the map's center:
    center = f"{user_lat},{user_lng}"

    # Create the URL for the static map:
    static_map_url = (
        "https://maps.googleapis.com/maps/api/staticmap"
        f"?center={center}"
        "&zoom=12"
        "&size=600x400"
        f"{markers_str}"
        f"&key={key}"
    )

    #creates results (list of dictionaries) each containing dist, place obj from top 3 results
    #this is then passed into places_list.html template
    context = {
        'address': address,
        'user_lat': user_lat,
        'user_lng': user_lng,
        'results': [
            {
                'distance': d,
                'place': p,
                'lat': float(p.latitude),
                'lng': float(p.longitude),
            } for (d, p) in top_3
        ]
    }

    return render(request, 'places_list.html', context)
