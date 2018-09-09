# blog_test

##  Notes
From tutorial 2: 

```python
python manage.py sqlmigrate polls_v2 0001
```
used to check the makemigration query from the `polls_v2` app

Creating database for app sequence:
1. `makemigrations polls_v2` prepare the migration
2. `migrate` to migrate everything to the database

### Shell testing
```python
from polls_v2.models import Choice, Question
from django.utils import timezone
Question.objects.all()
q = Question(question_text="What's new?", pub_date=timezone.now())
q.save()
q.id
q.question_text
q.pub_date
q.question_text = "What's up?"
q.save()
Question.objects.all()
```

```python
from polls_v2.models import Choice, Question
from django.utils import timezone
Question.objects.all()
Question.objects.filter(id=1)
Question.objects.filter(question_text__startswith='What')
current_year = timezone.now().year
Question.objects.get(pub_date__year=current_year)
Question.objects.get(id=2)
Question.objects.get(pk=1)
q = Question.objects.get(pk=1)
q.was_published_recently()
q.choice_set.all()
q.choice_set.create(choice_text='Not much', votes=0)
q.choice_set.create(choice_text='The sky', votes=0)
c = q.choice_set.create(choice_text='Just hacking again', votes=0)
c.question
q.choice_set.all()
q.choice_set.count()
Choice.objects.filter(question__pub_date__year=current_year)
c = q.choice_set.filter(choice_text__startswith='Just hacking')
c.delete()
```

###How to namespace: 

in mysite\urls, put inside urlpatterns these lines below:  
```python
path('polls_v2/', include('polls_v2.urls', namespace='polls_v2'))
```
Then, initialize a variable named `app_name` (the name must be this) and name it polls_v2. 

On the HTML Side, use something like this: 
```HTML
<li><a href="{% url 'polls_v2:detail' question.id %}">{{ question.question_text }}</a></li>
```