from django.shortcuts import render
import json
from django.http import HttpResponse,JsonResponse
from exercises.models.User.user_models import User
from exercises.models.Workout.workout_models import Movement
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from datetime import datetime
from exercises.serializers import UserSerializer
from http import HTTPStatus

# Get, Update, Delete Movement by id
def GUDMovement(request, id):
    movement = Movement.objects.get(pk=id)

    # Get a movement by id
    if(request.method == 'GET'):
        res_json = serializers.serialize("json", [movement])
        return HttpResponse(res_json, content_type='application/json')