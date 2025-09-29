from django.shortcuts import render
import json
from django.http import HttpResponse,JsonResponse
from exercises.models.Workout.workout_models import Workout, Exercise, Movement
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

        new_workout = Workout(
            gym = req_json['gym'],
            started = datetime.now(),
            label = req_json['label'],
            notes = req_json['notes'],
            user = user
        )
        new_workout.save()

        new_workout = Workout.objects.get(pk=new_workout.id)
        res_json = serializers.serialize("json", [new_workout])
    
        return HttpResponse(res_json, content_type='application/json')
            


@csrf_exempt
def workout(request, id):
    if not(Workout.objects.filter(pk=id)):
        return HttpResponse("{\"error\": \"Workout does not exist\"}", content_type='application/json')
    workout = Workout.objects.get(pk=id)

    # Get a workout by id
    if(request.method == 'GET'):
        res_json = serializers.serialize("json", [workout])
        return HttpResponse(res_json, content_type='application/json')

    # update an existing workout
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

# get all exercises with given workout id
def workoutExercise(request, id):
    exercises = Exercise.objects.filter(workout=id)

    if(request.method == 'GET'):
        res_json = serializers.serialize("json", exercises)
        return HttpResponse(res_json, content_type='application/json')