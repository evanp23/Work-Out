from rest_framework import serializers
from exercises.models.User.user_models import User
from exercises.models.Workout.workout_models import Workout

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class WorkoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workout
        fields = '__all__'
