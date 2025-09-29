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
def createSet(request):
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