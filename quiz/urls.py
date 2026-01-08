from django.urls import path
from .views import quiz_view, leaderboard, export_results, googler_quiz,  qualified_list

urlpatterns = [
    path('', quiz_view, name='quiz'),
    path('leaderboard/<str:round_name>/', leaderboard, name='leaderboard'),
    path('export/<str:round_name>/', export_results, name='export'),
    path('googler/', googler_quiz, name='googler'),
    path('qualified/', qualified_list, name='qualified'),


]
