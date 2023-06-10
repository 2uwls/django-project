from django.urls import path
from . import views

urlpatterns=[
    path('list/',views.question_list,name='question_list'),
    path('write/',views.question_write),
    path('detail/<int:question_id>/',views.question_detail,name='question_detail'),
    path('answer_write/<int:question_id>/',views.answer_write,name='answer_write'),
    path('modify/<int:question_id>/', views.question_modify, name='question_modify'),
    path('delete/<int:question_id>/',views.question_delete, name='question_delete'),
    path('answer/modify/<int:answer_id>/', views.answer_modify, name='answer_modify'),
    path('answer/delete/<int:answer_id>/',views.answer_delete, name='answer_delete'),
    


    
]