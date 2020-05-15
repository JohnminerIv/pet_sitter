from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import Pet, Appointment
from .forms import PetForm, AppointmentForm
from django.utils import timezone

"""
Home page - /
Must link to Pets List page & Calendar page
"""


def index(request):
    return render(request, 'index.html')


"""
Pets List page - pets/
Must list all of the user’s Pets in bullet points or list items
Pet names must link to their detail pages using the {% url %} template tag
Must include a form to create a new pet -OR- link to a separate pet creation page
Should not be viewable by non-logged-in users
"""


class PetListView(LoginRequiredMixin, ListView):
    """ Renders a list of all Users pets. """
    login_url = reverse_lazy('login')
    model = Pet

    def get(self, request):
        """GET a list of pets."""
        context = {
            'pets': self.get_queryset().filter(owner=request.user),
            'form': PetForm(request.POST)
        }
        return render(request, 'pets_list.html', context)

    def post(self, request):
        """Add a new pet."""
        form = PetForm(request.POST)
        if form.is_valid:
            pet = form.save(commit=False)
            pet.owner = request.user
            pet.save()
            messages.success(request, f'{pet.name} Added')
        else:
            messages.error(request, 'Could not add your pet.')
        context = {
            'pets': self.get_queryset().filter(owner=request.user),
            'form': form,
        }
        return render(request, 'pets_list.html', context)


"""
Pets Detail page - pets/<pet_id>
Must show all relevant details about that pet
Must list all appointments associated with that pet
Should not be viewable by non-logged-in users
"""


class PetDetailView(DetailView):
    """ Renders a specific page based on it's slug."""
    model = Pet

    def get(self, request, pet_id):
        """ Returns a specific wiki page by slug. """
        context = {
          'pet': self.get_queryset().get(id=pet_id),
          'appointments': Appointment.objects.filter(pet__id=pet_id)
        }
        return render(request, 'pet_detail.html', context)


"""
Calendar Page - calendar/
Must show all upcoming appointments with all pets, ordered by soonest first
Should not show appointments that have already occurred (hint: Look at the Polls Tutorial for how to do this!)
Must include a form to create a new appointment -OR- link to a separate appointment creation page
Should not be viewable by non-logged-in users
"""


class AppointmentListView(LoginRequiredMixin, ListView):
    """ Renders a list of all Users Appointments. """
    login_url = reverse_lazy('login')
    model = Appointment

    def get(self, request):
        """GET a list of appointment."""
        context = {
            'appointments': self.get_queryset().filter(
                        date_of_appointment__gte=timezone.now()
                        ).filter(pet__owner=request.user).order_by('pub_date'),
            'form': AppointmentForm(request.POST)
        }
        return render(request, 'appointment_list.html', context)

    def post(self, request):
        """Add a new Appointment."""
        form = PetForm(request.POST)
        if form.is_valid:
            appointment = form.save(commit=False)
            appointment.save()
            messages.success(request, 'Appoint Added')
        else:
            messages.error(request, 'Could not add your appointment.')
        context = {
            'appointments': self.get_queryset().filter(
                        date_of_appointment__gte=timezone.now()
                        ).filter(pet__owner=request.user).order_by('pub_date'),
            'form': form,
        }
        return render(request, 'appointment_list.html', context)


"""
Login page
Sign-up page
"""
