import os 
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

from PIL import Image
from django.db.models.signals import post_save


def user_directory_path_user_profile(instance, filename):
	profile_picture_name = 'users/{0}/profile.jpg'.format(instance.user.username)
	full_path = os.path.join(settings.MEDIA_ROOT, profile_picture_name)

	if os.path.exists(full_path):
		os.remove(full_path)

	return profile_picture_name

class UserProfile(AbstractUser):
	stripe_costumer = models.CharField(max_length=50)

class Profile(models.Model):
	user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='profile')
	phone = models.CharField('Phone Number', max_length=50, blank=True, null=True)
	short_description = models.TextField(blank=True, null=True)
	profile_picture = models.ImageField(default="users/default_profile.png",upload_to=user_directory_path_user_profile,blank=True, null=True)

	def __str__(self):
		return self.user.username

class AnonymousUser(models.Model):
	hostname = models.CharField('Hostname',blank=True,null=True,max_length=50)
	ip_address = models.GenericIPAddressField(protocol="ipv4")
	created_date = models.DateField(auto_now_add=True)
	class Meta:
		ordering = ['-created_date']

	def __str__(self):
		return '{}'.format(self.created_date, self.ip_address)

class Room(models.Model):
	speaker = models.ForeignKey(Profile, on_delete=models.CASCADE)
	anonymousUser=models.ForeignKey(AnonymousUser, on_delete=models.CASCADE)
	
	def __str__(self):
		return self.speaker.username


def create_user_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)

def save_user_profile(sender, instance, **kwargs):
	instance.profile.save()

post_save.connect(create_user_profile, sender=UserProfile)
post_save.connect(save_user_profile, sender=UserProfile)