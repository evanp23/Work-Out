from django.urls import path

from exercises.views.User import user_views
from exercises.views.Workout import workout_views
from exercises.views.Exercise import exercise_views

urlpatterns = [
    path("user/", user_views.createUser, name="createOrUpdateUser"),
    path("user/<int:id>/", user_views.user, name="GUDUser"),
    path("user/<int:id>/workout/", user_views.userWorkout, name="userWorkout"),
    path("workout/", workout_views.createWorkout, name="createWorkout"),
    path("workout/<int:id>/", workout_views.workout, name="GUDWorkout"),
    path("workout/<int:id>/exercise/", workout_views.workoutExercise, name="workoutExercise"),
    path("exercise/", exercise_views.createExercise, name="createExercise"),
    path("exercise/<int:id>/", exercise_views.exercise, name="GUDExercise"),
]