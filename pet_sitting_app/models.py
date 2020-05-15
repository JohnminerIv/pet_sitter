from django.contrib.auth.models import User
from django.db import models


class Pet(models.Model):
    """docstring for Pet."""
    pet_name = models.CharField(max_length=50, help_text="Name of your pet.")
    species = models.CharField(max_length=20, help_text="Species of your pet.")
    breed = models.CharField(max_length=20, help_text="Breed of your pet.")
    weight_in_pounds = models.IntegerField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE,
                              help_text="The owner of this pet.")


class Appointment(object):
    """docstring for Appointment."""
    date_of_appointment = models.DateField()
    duration_minutes = models.IntegerField()
    special_instructions = models.TextField()
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE,
                            help_text="Pet that the appointment is for.")
