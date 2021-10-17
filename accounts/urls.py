from django.urls import path
from .views import *
app_name = 'accounts'
urlpatterns = [
	
	path('profile/<username>/', UserProfile.as_view(), name="profile"),
	path('profile/edit', editProfile, name='edit'),

]