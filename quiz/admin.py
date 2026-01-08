from django.contrib import admin
from django import forms
from .models import Question, Result, QuizControl


# ✅ Custom Admin Form with Conditional Validation
class QuestionAdminForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = "__all__"

    def clean(self):
        cleaned_data = super().clean()
        question_type = cleaned_data.get("question_type")

        if question_type == "MCQ":
            # MCQ requires options and correct_option
            for field in ["option1", "option2", "option3", "option4", "correct_option"]:
                if not cleaned_data.get(field):
                    self.add_error(field, "This field is required for MCQ questions.")

        elif question_type == "TEXT":
            # TEXT requires correct_text_answer only
            if not cleaned_data.get("correct_text_answer"):
                self.add_error(
                    "correct_text_answer",
                    "This field is required for TEXT questions."
                )

        return cleaned_data


# ✅ Question Admin uses custom form
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    form = QuestionAdminForm
    list_display = ("text", "round_type", "question_type")
    list_filter = ("round_type", "question_type")


# ✅ Other models
admin.site.register(Result)
admin.site.register(QuizControl)
