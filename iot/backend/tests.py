from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase ,APIClient
from rest_framework import status 
from .models import Customer

class IOTAPITestCase(APITestCase):
    def setUp(self) -> None:
        self.sample_data=[{
                "timestamp": "2022-01-21T10:56:18.950901",
                "reading": 0.63,
                "device_id": "71bf19cb-e7e7-4334-af31-5ebba56a655d",
                "customer_id": "b0c2bda5-0d6d-4c6a-86d4-76489ea2b9df"
            },
            {
                "timestamp": "2022-01-21T10:57:18.950901",
                "reading": 0.9,
                "device_id": "71bf19cb-e7e7-4334-af31-5ebba56a655d",
                "customer_id": "b0c2bda5-0d6d-4c6a-86d4-76489ea2b9df"
            },
            {
                "timestamp": "2022-01-21T10:58:18.950901",
                "reading": 0.9,
                "device_id": "71bf19cb-e7e7-4334-af31-5ebba56a655d",
                "customer_id": "b0c2bda5-0d6d-4c6a-86d4-76489ea2b9df"
            },
            {
                "timestamp": "2022-01-21T10:59:18.950901",
                "reading": 0.32,
                "device_id": "71bf19cb-e7e7-4334-af31-5ebba56a655d",
                "customer_id": "b0c2bda5-0d6d-4c6a-86d4-76489ea2b9df"
            },
            {
                "timestamp": "2022-01-21T11:00:18.950901",
                "reading": 0.96,
                "device_id": "1cf67335-0793-42ad-80f3-3156cabc9da9",
                "customer_id": "b0c2bda5-0d6d-4c6a-86d4-76489ea2b9df"
            },
            {
                "timestamp": "2022-01-21T11:01:18.950901",
                "reading": 0.45,
                "device_id": "1cf67335-0793-42ad-80f3-3156cabc9da9",
                "customer_id": "b0c2bda5-0d6d-4c6a-86d4-76489ea2b9df"
            },
            {
                "timestamp": "2022-01-21T11:02:18.950901",
                "reading": 0.55,
                "device_id": "1cf67335-0793-42ad-80f3-3156cabc9da9",
                "customer_id": "b0c2bda5-0d6d-4c6a-86d4-76489ea2b9df"
            },
            {
                "timestamp": "2022-01-21T11:03:18.950901",
                "reading": 0.94,
                "device_id": "71bf19cb-e7e7-4334-af31-5ebba56a655d",
                "customer_id": "b0c2bda5-0d6d-4c6a-86d4-76489ea2b9df"
            },
            {
                "timestamp": "2022-01-21T11:04:18.950901",
                "reading": 0.61,
                "device_id": "94324014-0b4c-4b7e-840c-ff82f5304b06",
                "customer_id": "b0c2bda5-0d6d-4c6a-86d4-76489ea2b9df"
            },
            {
                "timestamp": "2022-01-21T11:05:18.950901",
                "reading": 0.09,
                "device_id": "71bf19cb-e7e7-4334-af31-5ebba56a655d",
                "customer_id": "b0c2bda5-0d6d-4c6a-86d4-76489ea2b9df"
            }]

        self.uname='customer1'
        self.pwd='User1@1234'
        self.customer_id = 'b0c2bda5-0d6d-4c6a-86d4-76489ea2b9df'
        user=User.objects.create(username=self.uname)
        user.set_password(self.pwd)
        # user.is_superuser=True
        user.save()
        # user.refresh_from_db()
        # user.customer.customer_id = 'b0c2bda5-0d6d-4c6a-86d4-76489ea2b9df'
        customer = Customer(user=user,customer_id=self.customer_id)
        customer.save()
        self.user=user
    
    def test_login(self):
        logged_in = self.client.login(username=self.uname,password=self.pwd)
        self.assertEquals(logged_in,True)
    
    def test_JWT(self):
        url = reverse('token_obtain_pair')
        self.user.is_active = False
        self.user.save()
        resp=self.client.post(url,{"username": self.uname, "password": self.pwd},format='json')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
        self.user.is_active = True
        self.user.save()
        resp=self.client.post(url,{"username": self.uname, "password": self.pwd},format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in resp.data and 'refresh' in resp.data)
        access_token=resp.data['access']

        verification_url = reverse('token_verify')
        resp = self.client.post(verification_url, {'token': access_token}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        resp = self.client.post(verification_url, {'token': 'abc'}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

        client = APIClient()
        url=reverse('api_device_create')
        client.credentials(HTTP_AUTHORIZATION='Bearer abc')
        resp = client.post(url, {}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_append_device_data(self):
        url = reverse('token_obtain_pair')
        resp=self.client.post(url,{"username": self.uname, "password": self.pwd},format='json')
        access_token=resp.data['access']
        client = APIClient()
        url=reverse('api_device_create')
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        resp = client.post(url,self.sample_data,format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)


    def test_get_device_data(self):
        url = reverse('token_obtain_pair')
        resp=self.client.post(url,{"username": self.uname, "password": self.pwd},format='json')
        access_token=resp.data['access']
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        url=reverse('api_device_create')
        resp = client.post(url,self.sample_data,format='json')
        url=reverse('api_devices')
        resp = client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue('device_id' in resp.data[0])
        self.assertTrue('customer_id' in resp.data[0])
        self.assertTrue('from' in resp.data[0])
        self.assertTrue('to' in resp.data[0])
        self.assertTrue('aggregation_size_minutes' in resp.data[0])
        self.assertTrue('aggregated_values' in resp.data[0])


