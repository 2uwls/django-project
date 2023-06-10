from django.db import models
from user.models import Member

class Question(models.Model):
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_dttm = models.DateTimeField()
    memberID = models.ForeignKey(Member, on_delete=models.CASCADE)
    class Meta:
        db_table = 'QUESTION'
    
class Answer(models.Model):
    content = models.TextField()
    create_dttm = models.DateTimeField()
    questionID = models.ForeignKey(Question, on_delete=models.CASCADE)
    writerID=models.CharField(max_length=15)
    class Meta:
        db_table = 'ANSWER'
