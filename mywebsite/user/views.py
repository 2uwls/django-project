from django.shortcuts import render, redirect
from .models import Member


def home(request) :
    print(request.session.get('user'))
    user=request.session.get('user',None)
    
    if user==None:
        return render(request,'home/index.html')

    user_data ={}
    user_data["user_id"] = user
    return render(request, 'home/index.html', user_data)

def login(request):
    if request.method == "GET":
        return render(request, 'login/login.html')
    
    elif request.method == "POST":
        memberID = request.POST['memberID'] 
        password = request.POST['password']
        
        try :
            check_id = Member.objects.get(memberID=memberID)
        except :
            check_id = False
            
        data_dic={}
        if not(memberID and password) :
            data_dic["err"] = "모든 값을 입력해 주세요." 
        elif check_id == False:
            data_dic["err"] = "등록된 아이디가 없습니다." 
        else :
            if password == check_id.password :
                request.session["user"] = check_id.memberID
                return redirect('/')
                data_dic["err"] = "로그인되었습니다."
                
            else :
                data_dic["err"] = "비밀번호가 잘못되었습니다." 
        return render(request, 'login/login.html', data_dic)
    
def logout(request):
    # if request.session.get("user"):
    #     del request.session["user]
    #     return redirect('/')
    
    # request.session.clear()
    request.session.flush()
    return redirect('/')

def register(request):
    if request.method=='GET':
        return render(request, 'register/register.html')
    elif request.method=='POST':
        print(request.POST) 
        print(type(request.POST))
        memberID = request.POST['memberID']
        password1 = request.POST['password1'] 
        password2 = request.POST['password2'] 
        name = request.POST['username']
        email = request.POST['exampleInputEmail1']
        
        try :
            check_id = Member.objects.get(memberID=memberID)
        except :
            check_id = False
            
        data_dic = {}
        
        if not(memberID and password1 and password2 and name and email) :
            data_dic["err"] = "모든 값을 입력해 주세요."
        elif check_id :
            print(check_id) 
            print(check_id.memberID) 
            print(check_id.password)
            data_dic["err"] = "이미 등록된 아이디 입니다."

        elif password1 != password2:
            data_dic["err"] = "비밀번호가 일치하지 않습니다."
        else:
            memberregister=Member(
            memberID=memberID, 
            password=password1, 
            name=name, 
            email=email,
            ) 
            memberregister.save()
            
            return redirect('/')
                    
                     
        return render(request, 'register/register.html', data_dic)
    
    
       