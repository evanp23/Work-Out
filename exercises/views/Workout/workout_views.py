from django.shortcuts import render
import json
from django.http import HttpResponse,JsonResponse
from exercises.models.Workout.workout_models import Workout
from exercises.models.User.user_models import User
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from datetime import datetime
from exercises.serializers import WorkoutSerializer
from http import HTTPStatus

@csrf_exempt
def createWorkout(request):
    req_json = json.loads(request.body.decode('utf-8'))

    #create a new workout
    if(request.method == 'POST'):
        user = User.objects.get(pk=req_json['user'])
        print(user)

        new_workout = Workout(
            gym = req_json['gym'],
            started = req_json['started'],
            completed = req_json['completed'],
            label = req_json['label'],
            notes = req_json['notes'],
            user = user
        )
        new_workout.save()

        new_workout = Workout.objects.get(pk=new_workout.id)
        res_json = serializers.serialize("json", [new_workout])
    
        return HttpResponse(res_json, content_type='application/json')
            

#Get or update workout by id
@csrf_exempt
def workout(request, id):
    if not(Workout.objects.filter(pk=id)):
        return HttpResponse("{\"error\": \"workout does not exist\"}", content_type='application/json')
    workout = Workout.objects.get(pk=id)

    # Get a workout
    if(request.method == 'GET'):
        res_json = serializers.serialize("json", [workout])
        return HttpResponse(res_json, content_type='application/json')

    #update an existing workout
    elif(request.method == 'PUT'):
        req_json = json.loads(request.body.decode('utf-8'))
        workout = Workout.jsonToWorkout(workout, req_json)
        workout.save()
        res_json = serializers.serialize("json", [workout])
        return HttpResponse(res_json, content_type='application/json')

    # Delete and existing workout
    elif(request.method == 'DELETE'):
        workout.delete()
        return HttpResponse(status=HTTPStatus.NO_CONTENT)