from django.test import TestCase
from django.contrib.auth.models import User
from .models import Pet, Appointment
from django.utils import timezone


class CanaryTestCase(TestCase):
    def test_true_is_true(self):
        """ Tests if True is equal to True. Should always pass. """
        self.assertEqual(True, True)


"""
Test Pets List page
Create User and Pet objects, log in
Load the page
Check if Pets belonging to the user appears in the result
"""


class PetListTestCase(TestCase):
    def test_pet_list_page(self):
        user = User()
        user.save()
        pet = Pet()
        pet.owner = user
        pet.pet_name = 'Alfred'
        pet.species = 'Dog'
        pet.breed = 'Type of dog'
        pet.weight_in_pounds = 75
        pet.save()
        self.client.force_login(user)
        response = self.client.get('/pets/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Alfred")


"""
Test Pets Detail page
Create User, Pet, and Appointment objects, log in
Load the page
Check if Pet object’s details appear in the result
"""
class PetDetailTestCase(TestCase):
    def test_pet_detail_page(self):
        user = User()
        user.save()
        pet = Pet()
        pet.owner = user
        pet.pet_name = 'Alfred'
        pet.species = 'Dog'
        pet.breed = 'Type of dog'
        pet.weight_in_pounds = 75
        pet.save()
        appointment = Appointment()
        appointment.date_of_appointment = timezone.now()
        appointment.duration_minutes = 50
        appointment.special_instructions = "Take care"
        appointment.pet = pet
        appointment.save()
        self.client.force_login(user)
        response = self.client.get(f'/pets/{pet.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Alfred")
        self.assertContains(response, "Take care")

"""
Test Pet Creation page
Create User object
Make a POST request to pets/ with key-value pairs to create a new Pet
Check that the Pet object was created in the database
"""

class AddPetTestCase(TestCase):
    def test_add_pet_page(self):
        user = User()
        user.save()
        pet_info = {
                'pet_name': 'Alfred',
                'species': 'Dog',
                'breed': 'Type of dog',
                'weight_in_pounds': 75
        }
        self.client.force_login(user)
        response = self.client.post('/pets/', pet_info)
        pet = Pet.objects.get(pet_name='Alfred')
        self.assertEqual(pet.pet_name, 'Alfred')

"""
Test Appointment Creation page
Create User and PET object
Make a POST request to calendar/ with key-value pairs to create a new Appointment
Check that the Appointment object was created in the database

"""
class AddAppointmentTestCase(TestCase):
    def test_add_appointment_page(self):
        user = User()
        user.save()
        pet = Pet()
        pet.owner = user
        pet.pet_name = 'Alfred'
        pet.species = 'Dog'
        pet.breed = 'Type of dog'
        pet.weight_in_pounds = 75
        pet.save()
        appointment_info = {
            'date_of_appointment': '10/20/2020',
            'duration_minutes': 5,
            'special_instructions': 'Take care',
            'pet': 1
        }
        self.client.force_login(user)
        response = self.client.post('/calendar/', appointment_info)
        appointment = Appointment.objects.get(pet__pet_name='Alfred')
        self.assertEqual(appointment.special_instructions, 'Take care')
