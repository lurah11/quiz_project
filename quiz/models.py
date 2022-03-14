from django.db import models

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=30)
    update = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.id}_{self.username}'

class Question(models.Model):
    text = models.CharField(max_length=200)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.id}_{self.text}'

class Option(models.Model):
    question = models.ForeignKey(Question,on_delete=models.CASCADE)
    text = models.CharField(max_length=100)
    is_true=models.BooleanField(default=False)

    def __str__(self):
        return f'Q_{self.question.id}_{self.text}_{self.is_true}'

class Answer(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    option = models.OneToOneField(Option,on_delete=models.CASCADE)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Q{self.user.username}_{self.option.id}_{self.option.is_true}'

class Result(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    result = models.FloatField()
    is_repeat = models.BooleanField(default=False)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id}.{self.user.username}_{self.result}_repeat={self.is_repeat}"

