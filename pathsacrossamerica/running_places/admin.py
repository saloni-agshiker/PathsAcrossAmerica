from django.contrib import admin
from .models import RunningPlace, Review
from .utils import validate_address
from django.contrib import messages
from django.db import transaction


@admin.register(RunningPlace)
class RunningPlaceAdmin(admin.ModelAdmin):
    exclude = ('latitude', 'longitude')

    @transaction.atomic
    def save_model(self, request, obj, form, change):
        lat, lng = validate_address(obj.address)
        if lat is None or lng is None:
            self.message_user(
                request,
                "Address could not be validated. Please enter a valid, deliverable address.",
                level=messages.ERROR
            )
            if change:
                # If updating an existing object, we might want to preserve the old valid location
                return
            # For new objects, just prevent saving — no need to delete
            return

        obj.latitude = lat
        obj.longitude = lng
        super().save_model(request, obj, form, change)
