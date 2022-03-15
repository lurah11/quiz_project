from django.shortcuts import render,redirect
from .models import *
from django.http import HttpResponse,JsonResponse
import random


# Create your views here.
def home(request):

    return render(request,'quiz/home.html')

def question_list_view(request):
    questions = Question.objects.all()
    context = {
        'questions':questions
    }
    return render(request,'quiz/question_list.html',context)

def question_detail_view(request,id):
    if request.method == 'POST':
        question = Question.objects.get(id=id)
        new_question = request.POST.get('text-area-question')
        question.text = new_question
        question.save()
        new_right_answer_id = request.POST.get('radio-option-input')
  
        for option in question.option_set.all():
            new_text = request.POST.get(f'option-input-{option.id}')
            option.text = new_text
            if option.id == int(new_right_answer_id):
                option.is_true = True
            else : 
                option.is_true = False
            option.save()
    question = Question.objects.get(id=id)
    context = {
        'question':question
    }
    return render(request,'quiz/question_detail.html',context)

def add_option_view(request,id):
    question = Question.objects.get(id=id)
    new_option = Option(question=question,text="Pilihan baru") 
    new_option.save()   
    return redirect('quiz:question-detail-view',id)

def delete_option_view(request,id,q_id):
    option = Option.objects.get(id=id)
    option.delete()
    return redirect('quiz:question-detail-view',q_id)

def add_question_view(request):
    new_question = Question(text="Buat Pertanyaan disini ya")
    new_question.save()
    new_option = Option(question=new_question,text="Pilihan baru",is_true=True)
    new_option.save()
    context = {
        'question': new_question
    }
    return redirect('quiz:question-detail-view',new_question.id)

def do_quiz_view(request):
    if request.method == "POST":
        # get the options that are the right answers : 
        list_right_option = []
        list_question = request.POST.get("question")
        list_question_id = list_question.split(',')
        for question_id in list_question_id:
            right_option = Option.objects.get(question__id=question_id,is_true=True)
            list_right_option.append(right_option.id)

        #get the list of answer from users and mark them
        right_answer = 0
        list_option_id = []
        q_count = int(request.POST.get("hidden_count"))
        username = request.POST.get("input-username")
        try : 
            user = User.objects.get(username=username.lower())
        except : 
            user = User(username=username.lower())
            user.save()
        try : 
            answer_object_list = Answer.objects.filter(user=user)
            answer_object_list.delete()
            print("Delete success")
        except:
            print("lalalalal")
        for q in range(1,q_count+1) :
            try:
                print(f"right answer{right_answer}")
                option_id = int(request.POST.get(f"radio_option_{q}"))
                print(f"option id : {option_id}")
                option = Option.objects.get(id=option_id)
                list_option_id.append(option_id)
                answer = Answer(user=user,option=option)
                print(answer)
                answer.save()
                if option.is_true == True : 
                    right_answer += 1
                    print(f"right answer{right_answer}")
            except Exception as e:
                print("masuk exception 1")
                print(e)
                right_answer = right_answer

        mark = (right_answer/q_count)*100

        #Save to Database and prevent duplicated username

        try : 
            update_result = Result.objects.get(user=user)
            update_result.result = mark 
            update_result.is_repeat = True 
            update_result.save()
        except :
            update_result = Result(user=user,result=mark)
            update_result.save()       

        # Render Response as JSON

        context = {
            'username':user.username,
            'mark':mark,
            'count':q_count,
            'list_right_option':list_right_option,
            'list_option_id':list_option_id
        }
        return JsonResponse(context)

    q_final = get_random_question()
    context = {
        'questions':q_final
    }
    print(q_final)
    return render(request,'quiz/do_quiz.html', context)

def get_random_question() : 
    q_all = Question.objects.all()
    last_question = q_all.last()
    last_q_id = last_question.id
    q_final = Question.objects.none()
    while q_final.count() < 2 :
            random_id = random.sample(range(1,last_q_id+1),1)
            selected_q = Question.objects.filter(id=random_id[0])
            q_final |= selected_q
    return q_final

def result_list_view(request):
    users = User.objects.all()
    context = {
        'users':users
    }
    return render (request,'quiz/result_list.html',context)

def question_delete_view(request,id):
    question = Question.objects.get(id=id)
    question.delete()
    return redirect('quiz:question-list-view')