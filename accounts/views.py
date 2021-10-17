import socket
import urllib.request
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, ListView, CreateView, UpdateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from .models import *
from .forms import *

User= get_user_model()

hostname = socket.gethostname()
ip = urllib.request.urlopen('http://ident.me').read().decode('utf8')

class Index(View):
	def get(self, request):
		anonymoususer = AnonymousUser.objects.create(ip_address=ip, hostname=hostname)
		anonymoususer.save()
	
		return render(request, 'pages/index.html')



class Dashboard(LoginRequiredMixin,View):
	def get(self, request):
		users = Profile.objects.all()
		an = AnonymousUser.objects.all()
		data = {
		'anonymous':an,
		'all':users
		}
		return render(request, 'pages/dash.html', data)


class UserProfile(LoginRequiredMixin,View):
	def get(self, request, username, *args, **kwargs):
		user = get_object_or_404(User, username=username)
		profile = Profile.objects.get(user=user)

		data = {
		'user':user,
		'profile':profile
		}
		return render(request, 'pages/profile.html', data)

@login_required
def editProfile(request):
	user = request.user.id
	profile = Profile.objects.get(user__id=user)
	user_info = User.objects.get(id=user)

	if request.method == 'POST':
		form = EditUserProfileForm(request.POST, request.FILES, instance=profile)
		if form.is_valid():
			user_info.first_name = form.cleaned_data.get('first_name')
			user_info.last_name = form.cleaned_data.get('last_name')
			
			profile.phone = form.cleaned_data.get('phone')
			profile.short_description = form.cleaned_data.get('short_description')
			profile.profile_picture = form.cleaned_data.get('profile_picture')

			profile.save()
			user_info.save()

			return redirect('users:profile', username=request.user.username)

	else:
		form = EditUserProfileForm(instance=profile)
	data = {
	'form':form
	}
	return render(request, 'components/modal.html', data)

