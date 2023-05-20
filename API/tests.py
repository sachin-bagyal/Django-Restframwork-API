from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Employee

class EmployeeAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_employee(self):
        data = {
            'name': 'Ram Mishra',
            'age': 35,
            'gender': 'M',
            'department': 'IT',
            'salary': '5000.00',
        }
        response = self.client.post('/api/employees/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Employee.objects.count(), 1)
        self.assertEqual(Employee.objects.get().name, 'Ram Mishra')

    def test_get_all_employees(self):
        Employee.objects.create(
            name='Ram Mishra',
            age=35,
            gender='M',
            department='IT',
            salary='5000.00'
        )
        Employee.objects.create(
            name='Jane Smith',
            age=40,
            gender='F',
            department='HR',
            salary='6000.00'
        )
        response = self.client.get('/api/employees/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_employee_by_id(self):
        employee = Employee.objects.create(
            name='Ram Mishra',
            age=35,
            gender='M',
            department='IT',
            salary='5000.00'
        )
        response = self.client.get(f'/api/employees/{employee.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Ram Mishra')

    def test_update_employee(self):
        employee = Employee.objects.create(
            name='Ram Mishra',
            age=35,
            gender='M',
            department='IT',
            salary='5000.00'
        )
        data = {
            'name': 'Ram Mishra Jr.',
            'age': 36,
            'gender': 'M',
            'department': 'IT',
            'salary': '5500.00',
        }
        response = self.client.put(f'/api/employees/{employee.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Employee.objects.get().name, 'Ram Mishra Jr.')

    def test_delete_employee(self):
        employee = Employee.objects.create(
            name='Ram Mishra',
            age=35,
            gender='M',
            department='IT',
            salary='5000.00'
        )
        response = self.client.delete(f'/api/employees/{employee.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Employee.objects.count(), 0)
