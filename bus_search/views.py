from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from .forms import SearchForm

from requests.auth import HTTPBasicAuth
from requests import Session
from zeep import Client
from zeep.transports import Transport
from zeep.exceptions import Fault
from zeep import helpers
import json

session = Session()
session.auth = HTTPBasicAuth('wsuser', 'sales')
url = 'http://dev.avibus.pro/UEEDev/ws/SalePort?wsdl'
client = Client(url, transport=Transport(session=session))


@csrf_exempt
def find_bus(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            departure = form.cleaned_data['departure']
            destination = form.cleaned_data['destination']
            trips_date = form.cleaned_data['trips_date']

            try:
                trips = client.service.GetTrips(Departure=departure,
                                                Destination=destination,
                                                TripsDate=trips_date)
                trips_dict = helpers.serialize_object(trips, dict)
                return JsonResponse(trips_dict)
            except Fault as fault:
                xml = fault.message
                i = xml.find('<errordescription>') + 18
                j = xml.find('</errordescription>')
                if j == -1:
                    message = xml
                else:
                    message = xml[i:j]
                return JsonResponse({'error': message}, status=400)
    else:
        form = SearchForm()

    return render(request, 'find_bus.html', {'form': form})
