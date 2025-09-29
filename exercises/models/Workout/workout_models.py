from django.db import models
from ..User.user_models import User

class Workout(models.Model):
    gym = models.CharField(max_length=500, null=True, blank=True)
    started = models.DateTimeField("date started")
    completed = models.DateTimeField("date completed")
    label = models.CharField(max_length=1000, null=True, blank=True)
    notes = models.CharField(max_length=32000, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering=['id']
    
    def __str__(self):
        return ("WORKOUT: " + self.gym)

    def jsonToWorkout(workout, json):
        workout.gym = json['gym'] if "gym" in json else workout.gym
        workout.started = json['started'] if "started" in json else workout.started
        workout.completed = json['completed'] if "completed" in json else workout.completed
        workout.label = json['label'] if "label" in json else workout.label
        workout.notes = json['notes'] if "notes" in json else workout.notes

        return workout

class Movement(models.Model):
    name = models.CharField(max_length=500)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    date_created = models.DateTimeField("date created")
    category = models.CharField(max_length=500, null=True, blank=True)

class Exercise(models.Model):
    movement = models.ForeignKey(Movement, on_delete=models.CASCADE)
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    date_created = models.DateTimeField("date created")
    time_spent_s = models.IntegerField()
    label = models.CharField(max_length=1000, null=True, blank=True)
    notes = models.CharField(max_length=32000, null=True, blank=True)

    def jsonToExercise(exercise, json):
        exercise.movement = json['movement'] if "movement" in json else exercise.movement
        exercise.workout = json['workout'] if "workout" in json else exercise.workout
        exercise.date_created = json['date_created'] if "date_created" in json else exercise.date_created
        exercise.time_spent_s = json['time_spent_s'] if "time_spent_s" in json else exercise.time_spent_s
        exercise.label = json['label'] if "label" in json else exercise.label
        exercise.notes = json['notes'] if "notes" in json else exercise.notes

        return exercise

class Set(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    set_num = models.IntegerField()
    reps = models.IntegerField(null=True, blank=True)
    weight = models.IntegerField(null=True, blank=True)
    date_time = models.DateTimeField("date created")
    notes = models.CharField(max_length=32000, null=True, blank=True)






