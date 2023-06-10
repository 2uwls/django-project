from django.shortcuts import render, redirect, get_object_or_404
from .models import Question, Answer
from user.models import Member
from django.utils import timezone
from .models import Answer
from django.http import HttpResponse
from django.contrib import messages
from django import forms
from django.urls import reverse
from django.core.paginator import Paginator 
from django.db.models import Q


def question_list(request):
    page = request.GET.get('page', '1')  # 페이지
    kw=request.GET.get('kw','')
    question_list = Question.objects.order_by('-create_dttm')
    
    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |  # 제목 검색
            Q(content__icontains=kw)  # 내용 검색
        ).distinct()

    paginator = Paginator(question_list, 5)
    page_obj = paginator.get_page(page)
    
    
    user_id = request.session.get("user")
    context = {
        'question_list': page_obj,
        'page': page,
        'kw': kw,
        'user_id': user_id,

    }
    
    return render(request, 'qna/question_list.html', context)

def question_write(request) :
    if request.method == "GET" :
        data_dic ={}
        data_dic["user_id"] = request.session["user"]
        return render(request, 'qna/question_write.html', data_dic)
    
    elif request.method == "POST" :
        memberID = request.POST['memberID']
        writer = Member.objects.get(memberID=memberID) 
        subject = request.POST['subject']
        content = request.POST['content']
        create_dttm= timezone.now()
        register=Question( subject=subject,
        content=content, create_dttm=create_dttm, memberID_id=writer.id,
        )
        register.save()
        return redirect('/qna/list')

def question_detail(request, question_id):
    try:
        user_id = request.session.get("user")
        contents = Question.objects.get(id=question_id)
        member = Member.objects.get(id=contents.memberID_id)
        answer_list = Answer.objects.filter(questionID_id=question_id).order_by('-create_dttm')
        data_dic = {"contents": contents, "memberID": member.memberID, "user_id": user_id, "answer_list": answer_list}
    except Question.DoesNotExist:
        return HttpResponse("Question does not exist.")
    except Member.DoesNotExist:
        return HttpResponse("Member does not exist.")
    except Answer.DoesNotExist:
        contents = Question.objects.get(id=question_id)
        member = Member.objects.get(id=contents.memberID_id)
        answer_list = []
        data_dic = {"contents": contents, "memberID": member.memberID, "answer_list": answer_list}

    return render(request, 'qna/question_detail.html', data_dic)

def answer_write(request, question_id) : 
    user_id = request.session["user"]
    content = request.POST["content"] 
    create_dttm = timezone.now() 
    questionID = question_id
    writerID = user_id
    
    register = Answer(
    content = content,
    create_dttm = create_dttm, 
    questionID_id = questionID,
    writerID = writerID
    )
    
    register.save()
    
    q=str(question_id)
    return redirect('/qna/detail/'+q)

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['subject', 'content']
        

def question_modify(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.save()
            return redirect('question_detail', question_id=question.id)
    else:
        form = QuestionForm(instance=question)

    # Include user_id and form in the context
    user_id = request.session.get("user")
    context = {'form': form, 'user_id': user_id}
    return render(request, 'qna/question_modify.html', context)

def question_delete(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    question.delete()
    
    return redirect(reverse('question_list'))  # 질문 목록 페이지로 리디렉션

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']

        
def answer_modify(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.method == "POST":
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.save()
            return redirect(reverse('question_detail', kwargs={'question_id': answer.questionID_id}))
    else:
        form = AnswerForm(instance=answer)
    
    user_id = request.session.get("user") 
    context = {'answer':answer,'form': form, 'user_id': user_id}
    return render(request, 'qna/answer_modify.html', context)


def answer_delete(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    answer.delete()
    
    return redirect(reverse('question_detail', kwargs={'question_id': answer.questionID_id}))













