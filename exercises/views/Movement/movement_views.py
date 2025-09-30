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
@csrf_exempt
def GUDMovement(request, id):
    if not(Movement.objects.filter(pk=id)):
        return HttpResponse("{\"error\": \"Movement does not exist\"}", content_type='application/json', status=HTTPStatus.NOT_FOUND)
    movement = Movement.objects.get(pk=id)

    # Get a movement by id
    if(request.method == 'GET'):
        res_json = serializers.serialize("json", [movement])
        return HttpResponse(res_json, content_type='application/json')

    # update an existing user
    elif(request.method == 'PUT'):
        req_json = json.loads(request.body.decode('utf-8'))
        movement = Movement.jsonToMovement(movement, req_json)
        movement.save()
        res_json = serializers.serialize("json", [movement])
        return HttpResponse(res_json, content_type='application/json')

    # delete user
    elif(request.method == 'DELETE'):
        movement.delete()
        return HttpResponse(status=HTTPStatus.NO_CONTENT)