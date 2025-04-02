from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import RunningPlace, Review


# Create your views here.
def add_place(request):
    template_data = {}
    template_data['title'] = 'Add Place'
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