from django.shortcuts import render
from django.http import HttpResponse
# import python dictionaries
from listings.choices import price_choices, bedroom_choices, state_choices
# fetch data from Listing model
from listings.models import Listing
# fetch data from Realtor model
from realtors.models import Realtor

# index is our index page... rendering index.html
def index(request):
    # assign data to variable.   use objects.order_by function and filter again. 
    # set max number to 3
    listings = Listing.objects.order_by('-list_date').filter(is_published=True)[:3]

    # create context variable and assign listings object.
    context = {
        'listings': listings,
        'state_choices': state_choices,
        'price_choices': price_choices,
        'bedroom_choices': bedroom_choices
    }

    return render(request, 'pages/index.html', context)

# about is our about.html page.
def about(request):
    #fetch all realtors
    realtors = Realtor.objects.order_by('-hire_date')
    
    # Get MVP
    mvp_realtors = Realtor.objects.all().filter(is_mvp=True)

    context = {
        'realtors': realtors,
        'mvp_realtors': mvp_realtors
    }

    return render(request, 'pages/about.html', context)