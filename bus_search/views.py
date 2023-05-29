from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

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
        obj = json.loads(request.body)
        departure_id = obj.get('departure')
        destination_id = obj.get('destination')
        date = obj.get('trips_date')
        try:
            trips = client.service.GetTrips(Departure=departure_id, Destination=destination_id, TripsDate=date)
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

    return JsonResponse(data={'error': 'method not allowed'}, status=405)
