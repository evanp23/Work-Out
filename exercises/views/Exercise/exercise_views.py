from django.shortcuts import render
import json
from django.http import HttpResponse,JsonResponse
from exercises.models.Workout.workout_models import Exercise, Movement, Workout, Set
from exercises.models.User.user_models import User
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from datetime import datetime
from exercises.serializers import ExerciseSerializer
from http import HTTPStatus

@csrf_exempt
def createExercise(request):
    req_json = json.loads(request.body.decode('utf-8'))

    #create a new exercise
    if(request.method == 'POST'):
        movement = Movement.objects.get(pk=req_json['movement'])
        workout = Workout.objects.get(pk=req_json['workout'])

        new_exercise = Exercise(
            movement = movement,
            workout = workout,
            date_created = datetime.now(),
            time_spent_s = req_json['time_spent_s'],
            label = req_json['label'],
            notes = req_json['notes']
        )
        new_exercise.save()

        new_exercise = Exercise.objects.get(pk=new_exercise.id)
        res_json = serializers.serialize("json", [new_exercise])
    
        return HttpResponse(res_json, content_type='application/json')
            


@csrf_exempt
def exercise(request, id):
    if not(Exercise.objects.filter(pk=id)):
        return HttpResponse("{\"error\": \"exercise does not exist\"}", content_type='application/json')
    exercise = Exercise.objects.get(pk=id)

    # Get an exercise by id
    if(request.method == 'GET'):
        res_json = serializers.serialize("json", [exercise])
        return HttpResponse(res_json, content_type='application/json')

    # update an existing exercise
    elif(request.method == 'PUT'):
        req_json = json.loads(request.body.decode('utf-8'))
        exercise = Exercise.jsonToExercise(exercise, req_json)
        exercise.save()
        res_json = serializers.serialize("json", [exercise])
        return HttpResponse(res_json, content_type='application/json')

    # Delete and existing exercise
    elif(request.method == 'DELETE'):
        exercise.delete()
        return HttpResponse(status=HTTPStatus.NO_CONTENT)
    
# get all sets with given exercise id
def exerciseSet(request, id):
    sets = Set.objects.filter(exercise=id)

    if(request.method == 'GET'):
        res_json = serializers.serialize("json", sets)
        return HttpResponse(res_json, content_type='application/json')