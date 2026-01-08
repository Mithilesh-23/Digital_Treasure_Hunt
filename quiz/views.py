from django.shortcuts import render
from django.utils import timezone
from .models import Question, Result, QuizControl
import random
from django.http import HttpResponse
from openpyxl import Workbook



def quiz_view(request):
    control = QuizControl.objects.first()

    if not control or not control.is_active:
        return render(request, 'quiz/wait.html')

    now = timezone.now()
    elapsed = (now - control.start_time).total_seconds()
    remaining = max(0, control.duration - int(elapsed))

    questions = list(Question.objects.all())
    random.shuffle(questions)

    if request.method == 'POST' and remaining >= 0:
        score = 0
        for q in questions:
            selected = request.POST.get(str(q.id))
            if selected and int(selected) == q.correct_option:
                score += 1

        name = request.POST.get('name')
        Result.objects.create(name=name, score=score)

        return render(request, 'quiz/result.html', {'score': score})

    return render(request, 'quiz/quiz.html', {
        'questions': questions,
        'remaining': remaining
    })

def leaderboard(request):
    results = Result.objects.order_by('-score', 'submitted_at')[:50]
    return render(request, 'quiz/leaderboard.html', {'results': results})


def export_results(request):
    results = Result.objects.order_by('-score', 'submitted_at')

    wb = Workbook()
    ws = wb.active
    ws.title = "Round 1 Results"

    # Header
    ws.append(["Rank", "Name", "Score", "Submission Time"])

    # Data
    for idx, r in enumerate(results, start=1):
        ws.append([idx, r.name, r.score, r.submitted_at.strftime("%Y-%m-%d %H:%M:%S")])

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = 'attachment; filename="round1_results.xlsx"'

    wb.save(response)
    return response