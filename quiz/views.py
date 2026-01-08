from django.shortcuts import render
from django.utils import timezone
from .models import Question, Result, QuizControl
import random
from django.http import HttpResponse
from openpyxl import Workbook


#  this function is for the round 1 
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
        Result.objects.create(name=name, score=score, round_type="ROUND1")
        mark_top50_round1()
        return render(request, 'quiz/result.html', {'score': score})

    return render(request, 'quiz/quiz.html', {
        'questions': questions,
        'remaining': remaining
    })

# this show the leader board
def leaderboard(request, round_name):
    results = Result.objects.filter(
        round_type=round_name
    ).order_by('-score', 'submitted_at')[:50]

    return render(request, 'quiz/leaderboard.html', {
        'results': results,
        'round_name': round_name
    })

def export_results(request, round_name):
    results = Result.objects.filter(
        round_type=round_name
    ).order_by('-score', 'submitted_at')

    wb = Workbook()
    ws = wb.active
    ws.title = f"{round_name} Results"

    ws.append(["Rank", "Name", "Score", "Submission Time"])

    for idx, r in enumerate(results, start=1):
        ws.append([idx, r.name, r.score, r.submitted_at.strftime("%Y-%m-%d %H:%M:%S")])

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = f'attachment; filename="{round_name}_results.xlsx"'

    wb.save(response)
    return response



# this function is for the googler round 
def googler_quiz(request):
    control = QuizControl.objects.first()

    if not control or not control.is_active:
        return render(request, 'quiz/wait.html')

    now = timezone.now()
    elapsed = (now - control.start_time).total_seconds()
    remaining = max(0, control.duration - int(elapsed))

    questions = list(Question.objects.filter(round_type='GOOGLER'))
    random.shuffle(questions)

    if request.method == 'POST' and remaining >= 0:
        score = 0

        for q in questions:
            if q.question_type == "MCQ":
                selected = request.POST.get(str(q.id))
                if selected and q.correct_option and int(selected) == q.correct_option:
                    score += 1
            else:  # TEXT question
                answer = request.POST.get(str(q.id), "").strip().lower()
                if q.correct_text_answer and answer == q.correct_text_answer.strip().lower():
                    score += 1

        name = request.POST.get('name')
        Result.objects.create(name=name, score=score, round_type="GOOGLER")


        return render(request, 'quiz/result.html', {'score': score})

    return render(request, 'quiz/googler_quiz.html', {
        'questions': questions,
        'remaining': remaining
    })
 


#  for selecting the top 50 
def mark_top50_round1():
    top50 = Result.objects.filter(
        round_type="ROUND1"
    ).order_by('-score', 'submitted_at')[:50]

    Result.objects.filter(round_type="ROUND1").update(qualified=False)

    for r in top50:
        r.qualified = True
        r.save()


def qualified_list(request):
    # 🔥 Recalculate top 50 every time page opens
    top50 = Result.objects.filter(
        round_type="ROUND1"
    ).order_by('-score', 'submitted_at')[:50]

    # Reset all
    Result.objects.filter(round_type="ROUND1").update(qualified=False)

    # Mark top as qualified
    for r in top50:
        r.qualified = True
        r.save()

    results = Result.objects.filter(
        round_type="ROUND1",
        qualified=True
    ).order_by('-score', 'submitted_at')

    return render(request, 'quiz/qualified.html', {'results': results})
