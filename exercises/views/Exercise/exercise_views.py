from django.shortcuts import render
import json
from django.http import HttpResponse,JsonResponse
from exercises.models.Workout.workout_models import Exercise, Movement, Workout
from exercises.models.User.user_models import User
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from datetime import datetime
from exercises.serializers import ExerciseSerializer
from http import HTTPStatus

@csrf_exempt
def createExercise(request):
    req_json = json.loads(request.body.decode('utf-8'))

    #create a new workout
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
def workout(request, id):
    if not(Workout.objects.filter(pk=id)):
        return HttpResponse("{\"error\": \"workout does not exist\"}", content_type='application/json')
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