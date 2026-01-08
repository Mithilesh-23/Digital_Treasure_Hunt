from django.urls import path
from .views import quiz_view, leaderboard, export_results

urlpatterns = [
    path('', quiz_view, name='quiz'),
    path('leaderboard/', leaderboard, name='leaderboard'),
    path('export/', export_results, name='export'),

]
