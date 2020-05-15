from django import forms
from .models import Pet, Appointment


class PetForm(forms.ModelForm):
    """ Render and process a form based on the Pet model. """
    class Meta:
        model = Pet
        fields = ('pet_name', 'species', 'breed', 'weight_in_pounds')


class AppointmentForm(forms.ModelForm):
    """ Render and process a form based on the Appointment model. """
    class Meta:
        model = Appointment
        fields = ('date_of_appointment', 'duration_minutes',
                  'special_instructions', 'pet')
