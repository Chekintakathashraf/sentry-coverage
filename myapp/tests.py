import pytest
from faker import Faker
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from myapp.models import User  # Ensure the correct import path for your User model
from django.core.exceptions import PermissionDenied
import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from django.core.exceptions import PermissionDenied

fake = Faker()

# Helper function to create a user and get an access token
def create_user_and_get_token():
    # Create a user
    user = User.objects.create_user(
        username='testuser', email='testuser@example.com', password='testpassword'
    )

    # Generate a JWT token for the created user
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    
    return user, access_token

@pytest.mark.django_db
def test_project_crud():
    client = APIClient()

    # Create user and get token
    user, access_token = create_user_and_get_token()

    # Add the JWT token to the Authorization header for authentication
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

    # CREATE a project
    project_name = fake.company()
    response = client.post(reverse('project-list-create'), {'name': project_name, 'owner': user.id})
    assert response.status_code == 201
    project_id = response.data['id']

    # READ the project
    response = client.get(reverse('project-detail', args=[project_id]))
    assert response.status_code == 200
    assert response.data['name'] == project_name

    # UPDATE the project
    updated_name = fake.company()
    response = client.put(reverse('project-detail', args=[project_id]), {'name': updated_name, 'owner': user.id})
    assert response.status_code == 200
    assert response.data['name'] == updated_name

    # DELETE the project
    response = client.delete(reverse('project-detail', args=[project_id]))
    assert response.status_code == 204



@pytest.mark.django_db
def test_sentry_integration():
    client = APIClient()

    try:
        response = client.get(reverse('sentry-debug'))
        assert response.status_code == 500
    except ZeroDivisionError:
        pass

    try:
        response = client.get(reverse('sentry-permission'))
        assert response.status_code == 403
    except PermissionDenied:
        pass

    try:
        response = client.get(reverse('sentry-value-error'))
        assert response.status_code == 500
    except ValueError:
        pass

    response = client.get(reverse('sentry-logging'))
    assert response.status_code == 500
