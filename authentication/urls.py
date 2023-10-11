# Importing necessary modules and views
from dj_rest_auth.jwt_auth import get_refresh_view
from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.views import LoginView, LogoutView, UserDetailsView
from django.urls import path
from rest_framework_simplejwt.views import TokenVerifyView
from allauth.socialaccount.views import signup
from authentication.views import GoogleLogin

# Define the URL patterns
urlpatterns = [
    # Route for user registration
    path("register/", RegisterView.as_view(), name="rest_register"),
    
    # Route for user login. 
    # Once authenticated, dj_rest_auth generates a JWT (JSON Web Token) for the user.
    path("login/", LoginView.as_view(), name="rest_login"),

    # Route for user logout.
    path("logout/", LogoutView.as_view(), name="rest_logout"),

    # Route to retrieve the details of the currently authenticated user.
    path("user/", UserDetailsView.as_view(), name="rest_user_details"),

    # Route to verify a token's validity.
    # If Next Auth sends a token to this endpoint and gets a successful response, the token is valid.
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),

    # Route to obtain a refreshed token.
    # JWT tokens have an expiry. When the current token is about to expire, 
    # Next Auth can fetch a new one from this endpoint without requiring the user to log in again.
    path("token/refresh/", get_refresh_view().as_view(), name="token_refresh"),

    # Route for Google OAuth login.
    # This leverages the allauth.socialaccount.providers.google integration to allow users to log in via their Google account.
    # After the user successfully logs in with Google, a JWT is generated and sent to Next Auth.
    path("google/", GoogleLogin.as_view(), name="google_login"),
]

