from django.urls import path
from . import views

app_name = 'quiz'

urlpatterns = [
    path('',views.home, name='home-view'),
    path('question_list',views.question_list_view,name='question-list-view'),
    path('question_detail/<int:id>',views.question_detail_view,name='question-detail-view'),
    path('add_option/<int:id>',views.add_option_view,name='add-option-view'),
    path('delete_option/<int:id>/<int:q_id>',views.delete_option_view,name='delete-option-view'),
    path('add_question',views.add_question_view,name='add-question-view'),
    path('do_quiz',views.do_quiz_view,name='do-quiz-view'),
    path('result_list',views.result_list_view,name='result-list-view'),
    path('delete_question/<int:id>',views.question_delete_view,name='question-delete-view')
]