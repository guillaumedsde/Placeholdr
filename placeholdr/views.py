from django.shortcuts import render
from django.http import HttpResponse
from placeholdr.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from datetime import datetime

# Import Trip
from placeholdr.models import Trip, TripNode

# Import Place
from placeholdr.models import Place

# Import the Category model
from placeholdr.models import Category

# Import the CategoryForm
from placeholdr.forms import CategoryForm

# Import the Page model
from placeholdr.models import Page

from placeholdr.models import UserProfile


# Import the PageForm
from placeholdr.forms import PageForm

def index(request):
	request.session.set_test_cookie()
	# Query the database for a list of ALL categories currently stored
	# Order the categories by number of likes in descending order
	# Retrieve the top 5 only - or all if less than 5
	# Place the list in our context_dict dictionary
	# that will be passed to the template engine
	# Construct a dictionary to pass to the template as its context.
	# Note the key boldmessage is the same as {{ boldmessage }} in the template!
	
	place_list = Place.objects.order_by('?')[:5]
	trip_list = Trip.objects.order_by('?')[:5]
	user_list = UserProfile.objects.select_related('user').order_by('-rep')[:7]
	
	context_dict = {'places' : place_list, 'users' : user_list, 'trips': trip_list}
	
	visitor_cookie_handler(request)
	
	context_dict['visits'] = request.session['visits']

	# Render the response and send it back!
	response = render(request, 'placeholdr/index.html', context_dict)

	# Return response back to user, updating any cookies that need changed
	return response

def about(request):
	if request.session.test_cookie_worked():
		print("TEST COOKIE WORKED!")
		request.session.delete_test_cookie()
		
	visitor_cookie_handler(request)
	context_dict = {'visits' : request.session['visits']}
	
	return render(request, 'placeholdr/about.html', context_dict)
	
def register(request):
	# Boolean for when registration was successful, false initially,
	# then set to true if successful
	registered = False

	# If it's a HTTP POST, we're interested in processing form data
	if request.method == 'POST':
		# Attempt to get information from the form
		user_form = UserForm(data=request.POST)
		profile_form = UserProfileForm(data=request.POST)

		# If the two forms are valid
		if user_form.is_valid() and profile_form.is_valid():
			# Save the user's form data to the database
			user = user_form.save()

			# Hash the password then update the user object
			user.set_password(user.password)
			user.save()

			profile = profile_form.save(commit=False)
			profile.user = user

			# Check if there's a profile picture
			if 'picture' in request.FILES:
				profile.picture = request.FILES['picture']

			# Sve the UserProfile model instance
			profile.save()

			registered = True

		else:

			print(user_form.errors, profile_form.errrors)
	else:
		user_form = UserForm()
		profile_form = UserProfileForm()

	return render(request,
				  'placeholdr/register.html',
				  {'user_form': user_form,
				   'profile_form':profile_form,
				   'registered': registered})

def user_login(request):
	# If the request is HTTP POST, try to get the relevant information
	if request.method == 'POST':
		# Use request.POST.get('<variable>') instead of .get['<v as
		# it returns None if the value does not exist instead of an error
		username = request.POST.get('username')
		password = request.POST.get('password')

		# Check if login combination is valid
		user = authenticate(username=username, password=password)

		# If we have a User object, the details are correct
		if user:
			# Is the account active?
			if user.is_active:
				# If valid and active, log in
				login(request, user)
				return HttpResponseRedirect(reverse('index'))
			else:
				# Inactive account
				return HttpResponse("Your Placeholdr account is disabled.")
		else:
			# Bad login details provided
			print("Invalid login details: {0}, {1}".format(username, password))
			return HttpResponse("Invalid login details supplied.")
	else:
		# Not a POST so display the login form
		return render(request, 'placeholdr/login.html', {})

@login_required
def restricted(request):
	return render(request, 'placeholdr/restricted.html', {})

@login_required
def user_logout(request):
	# Since we know they are logged in, we can log them out
	logout(request)
	return HttpResponseRedirect(reverse('index'))

# A helper method
def get_server_side_cookie(request, cookie, default_val=None):
	val = request.session.get(cookie)
	if not val:
		val = default_val
	return val

def visitor_cookie_handler(request):
	# If the cookie doesn't exist, the default value of 1 is used
	visits = int(get_server_side_cookie(request, 'visits', '1'))

	last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))
	last_visit_time = datetime.strptime(last_visit_cookie[:-7],
										'%Y-%m-%d %H:%M:%S')

	# If it's been more than a day since the last visit...
	if (datetime.now() - last_visit_time).days > 0:
		visits = visits + 1
		# Update the last visit cookie
		request.session['last_visit'] = str(datetime.now())
	else:
		request.session['last_visit'] = last_visit_cookie
		
	# Update/set the visits cookie
	request.session['visits'] = visits

def show_trip(request, trip_slug):
	# If the request is HTTP POST, try to get the relevant information
	if trip_slug:
		# Use request.POST.get('<variable>') instead of .get['<v as
		# it returns None if the value does not exist instead of an error


                print(Trip.objects.all()[0].slug)
                # Check if login combination is valid
                trip = Trip.objects.get(slug=trip_slug)
                
		# If we have a User object, the details are correct
                if trip:
                        places = []
                        trip_nodes = TripNode.objects.filter(tripId=trip)
                        if trip_nodes:
                                for trip_n in trip_nodes:
                                        places.append(trip_n.placeId)
                        return render(request,
				  'placeholdr/trip.html',
				  {'trip': trip, 'places':places, 'trip_nodes':trip_nodes})
                else:
                        return HttpResponse("Invalid trip slug supplied.")
	else:
		# Not a POST so display the login form
		return HttpResponseRedirect(reverse('index'))

def show_place(request, place_slug):
	# If the request is HTTP POST, try to get the relevant information
	if place_slug:
		# Use request.POST.get('<variable>') instead of .get['<v as
		# it returns None if the value does not exist instead of an error


                print(Place.objects.all()[0].slug)
                # Check if login combination is valid
                place = Place.objects.get(slug=place_slug)
                
		# If we have a User object, the details are correct
                if place:
                        return render(request,
				  'placeholdr/place.html',
				  {})
                else:
                        return HttpResponse("Invalid place slug supplied.")
	else:
		# Not a POST so display the login form
		return HttpResponseRedirect(reverse('index'))