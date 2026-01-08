from django.db import models

class Question(models.Model):
    text = models.CharField(max_length=255)
    option1 = models.CharField(max_length=255, blank=True, null=True)
    option2 = models.CharField(max_length=255, blank=True, null=True)
    option3 = models.CharField(max_length=255, blank=True, null=True)
    option4 = models.CharField(max_length=255, blank=True, null=True)

    correct_option = models.IntegerField(blank=True, null=True)

    option1_image = models.ImageField(upload_to='options/', blank=True, null=True)
    option2_image = models.ImageField(upload_to='options/', blank=True, null=True)
    option3_image = models.ImageField(upload_to='options/', blank=True, null=True)
    option4_image = models.ImageField(upload_to='options/', blank=True, null=True)


    ROUND_CHOICES = [
    ('ROUND1', 'Round 1'),
    ('GOOGLER', 'Googler Round'),
]

    QUESTION_TYPE_CHOICES = [
    ('MCQ', 'MCQ'),
    ('TEXT', 'Text Answer'),
]

    round_type = models.CharField(
    max_length=20,
    choices=ROUND_CHOICES,
    default='ROUND1'
)

    question_type = models.CharField(
    max_length=10,
    choices=QUESTION_TYPE_CHOICES,
    default='MCQ'
)
    correct_text_answer = models.CharField(
    max_length=255,
    blank=True,
    null=True
)

    question_image = models.ImageField(
    upload_to='questions/',
    blank=True,
    null=True
)
    


    def __str__(self):
        return self.text
    
class Result(models.Model):
    name = models.CharField(max_length=100)
    score = models.IntegerField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    round_type = models.CharField(max_length=20, default="ROUND1")
    qualified = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.name} - {self.score}"

    
class QuizControl(models.Model):
    is_active = models.BooleanField(default=False)
    duration = models.IntegerField(help_text="Duration in seconds")
    start_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return "Quiz Control"


