from django.shortcuts import render
import json
from django.http import HttpResponse,JsonResponse
from exercises.models.User.user_models import User
from exercises.models.Workout.workout_models import Movement, Workout
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from datetime import datetime
from exercises.serializers import UserSerializer
from http import HTTPStatus

@csrf_exempt
def createUser(request):
    req_json = json.loads(request.body.decode('utf-8'))

    #create a new user
    if(request.method == 'POST'):
        if(User.objects.filter(username = req_json['username'])):
            return HttpResponse("{\"error\": \"username already exists\"}", content_type='application/json')

        
        User(
            username = req_json['username'],
            first_name = req_json['firstName'],
            last_name = req_json['lastName'],
            email = req_json['email'],
            pwd = req_json['pwd'],
            date_joined = datetime.now()
        ).save()

        new_user = User.objects.get(username = req_json['username'])
        res_json = serializers.serialize("json", [new_user])
    
        return HttpResponse(res_json, content_type='application/json')
            

@csrf_exempt
def user(request, id):
    if not(User.objects.filter(pk=id)):
        return HttpResponse("{\"error\": \"user does not exist\"}", content_type='application/json', status=HTTPStatus.NOT_FOUND)
    user = User.objects.get(pk=id)

    # get user by id
    if(request.method == 'GET'):
        res_json = serializers.serialize("json", [user])
        return HttpResponse(res_json, content_type='application/json')

    # update an existing user
    elif(request.method == 'PUT'):
        req_json = json.loads(request.body.decode('utf-8'))
        user = User.jsonToUser(user, req_json)
        user.save()
        res_json = serializers.serialize("json", [user])
        return HttpResponse(res_json, content_type='application/json')

    # delete user
    elif(request.method == 'DELETE'):
        user.delete()
        return HttpResponse(status=HTTPStatus.NO_CONTENT)

# get all workouts with given user id
def userWorkout(request, id):
    if not(User.objects.filter(user=id)):
        return HttpResponse("{\"error\": \"User does not exist\"}", content_type='application/json', status=HTTPStatus.NOT_FOUND)
    workouts = Workout.objects.filter(user=id)

    if(request.method == 'GET'):
        res_json = serializers.serialize("json", workouts)
        return HttpResponse(res_json, content_type='application/json')
    
@csrf_exempt
def userMovement(request, id):
    if not(User.objects.filter(pk=id)):
        return HttpResponse("{\"error\": \"user does not exist\"}", content_type='application/json', status=HTTPStatus.NOT_FOUND)
    user = User.objects.get(pk=id)

    #create a new user
    if(request.method == 'POST'):
        req_json = json.loads(request.body.decode('utf-8'))
        new_movement = Movement(
            name = req_json['name'],
            created_by = user,
            date_created = datetime.now(),
            category = req_json['category']
        )
        new_movement.save()

        new_movement = Movement.objects.get(id=new_movement.id)
        res_json = serializers.serialize("json", [new_movement])
    
        return HttpResponse(res_json, content_type='application/json')
    
    # get all movements created by user
    elif(request.method == 'GET'):
        print('eeeeeeeeeellooooo')
        movements = Movement.objects.filter(created_by=user.id)
        print(movements)
        res_json = serializers.serialize("json", movements)
        return HttpResponse(res_json, content_type='application/json')