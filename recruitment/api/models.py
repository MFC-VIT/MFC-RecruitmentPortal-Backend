from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Domain(models.Model):
    domain_name = models.CharField(max_length=250)

    def __str__(self):
        return self.domain_name

class mcqQuestions(models.Model):
    domain = models.ForeignKey(Domain,on_delete=models.CASCADE,related_name="domain_mcq_questions")
    question_id = models.CharField(max_length=250, unique=True, primary_key=True)
    question = models.TextField()
    option_1 = models.CharField(max_length=500)
    option_2 = models.CharField(max_length=500)
    option_3 = models.CharField(max_length=500)
    option_4 = models.CharField(max_length=500)

    def __str__(self):
        return self.question

class typeQuestions(models.Model):
    domain = models.ForeignKey(Domain,on_delete=models.CASCADE,related_name="domain_type_questions")
    question_id = models.CharField(max_length=250, unique=True, primary_key=True)
    question = models.TextField()

    def __str__(self):
        return self.question

class Responses(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="user_responses")
    domain = models.ForeignKey(Domain,on_delete=models.CASCADE,related_name="domain_responses")
    question = models.TextField()
    answer = models.TextField()

    def __str__(self):
        return self.question
