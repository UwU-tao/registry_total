from .models import Owner, Vehicle, VehicleRegistration
from django.contrib.auth.models import User
from .serializers import UserSerializer, OwnerSerializer, VehicleSerializer, VehicleRegisSerializer
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
import tablib
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from django.http import JsonResponse
from django.core import serializers
import json
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication,)

@user_passes_test(lambda user: user.is_superuser)
class CreateUserView(generics.CreateAPIView):
    model = User
    serializer_class = UserSerializer

    def post(self, request, format='json'):
        serializer = serializers.UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                token = Token.objects.create(user=user)
                json = serializer.data
                json['token'] = token.key
                return Response(json, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# @api_view(['GET'])
# def view_data(request):
#     owner = Owner.objects.all()
#     regis = owner.vehicleregistration.all()
#     vehicle = regis.vehicle.all()
    
#     combined_data = []

#     for i, (owner_instance, vehicle_instance, vehicleregistration_instance) in enumerate(zip(owner, vehicle, regis)):
#         owner_serialized_data = json.loads(serializers.serialize('json', [owner_instance]))[0]['fields']
#         vehicle_serialized_data = json.loads(serializers.serialize('json', [vehicle_instance]))[0]['fields']
#         vehicleregistration_serialized_data = json.loads(serializers.serialize('json', [vehicleregistration_instance]))[0]['fields']

#         combined_instance = {
#             'inc': i + 1,  # Auto-increment ID
#             'Owner': owner_serialized_data,
#             'Vehicle': vehicle_serialized_data,
#             'VehicleRegis': vehicleregistration_serialized_data 
#         }

#         combined_data.append(combined_instance)

#     return JsonResponse(combined_data, safe=False)

@api_view(['GET'])
def view_data(request):
    owner = Owner.objects.all()
    regis = VehicleRegistration.objects.filter(owner__in=owner)
    vehicles = Vehicle.objects.filter(regis_code__in=regis)
    
    combined_data = []

    for i, (owner_instance, vehicleregistration_instance, vehicle_instance) in enumerate(zip(owner, regis, vehicles)):
        owner_serialized_data = json.loads(serializers.serialize('json', [owner_instance]))[0]['fields']
        vehicleregistration_serialized_data = json.loads(serializers.serialize('json', [vehicleregistration_instance]))[0]['fields']
        vehicle_serialized_data = json.loads(serializers.serialize('json', [vehicle_instance]))[0]['fields']

        combined_instance = {
            'inc': i + 1,  # Auto-increment ID
            'Owner': owner_serialized_data,
            'Regis': vehicleregistration_serialized_data,
            'Vehicle': vehicle_serialized_data
        }

        combined_data.append(combined_instance)

    return JsonResponse(combined_data, safe=False)
    
@csrf_exempt
def import_data(request):
    if request.method=='POST':
        dataset = tablib.Dataset()
        new_owners = request.FILES['excel_file']
        
        imported_data = dataset.load(new_owners.read(), format='xlsx')
        for data in imported_data:
            val1 = Owner(
                data[0], data[0], data[1], data[2], data[3], data[4], data[5], data[6]
            )
            val1.save()
            
            val3 = VehicleRegistration(
                data[23], data[23], data[24], data[25], data[26], data[0]
            )
            val3.save()
            
            val2 = Vehicle(
                data[7], data[7], data[8], data[9], data[10], data[11], data[12], data[13], data[14], data[15], data[16], data[17], data[18], data[19], data[20], data[21], data[23]
            )
            val2.save()
            
            
        return JsonResponse({'message': 'Import successful'})

    return JsonResponse({'error': 'Invalid request'})