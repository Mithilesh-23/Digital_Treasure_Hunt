from django.db import models

class Question(models.Model):
    text = models.CharField(max_length=255)
    option1 = models.CharField(max_length=100)
    option2 = models.CharField(max_length=100)
    option3 = models.CharField(max_length=100)
    option4 = models.CharField(max_length=100)
    correct_option = models.IntegerField()

    def __str__(self):
        return self.text
    
class Result(models.Model):
    name = models.CharField(max_length=100)
    score = models.IntegerField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.score}"

    
class QuizControl(models.Model):
    is_active = models.BooleanField(default=False)
    duration = models.IntegerField(help_text="Duration in seconds")
    start_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return "Quiz Control"


