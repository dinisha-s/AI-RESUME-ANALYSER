from django.db import models

class ResumeAnalysis(models.Model):

    uploaded_at = models.DateTimeField(auto_now_add=True)

    resume_text = models.TextField()

    ai_feedback = models.TextField()

    score = models.IntegerField(default=0)

    def __str__(self):
        return f"Analysis {self.id}"