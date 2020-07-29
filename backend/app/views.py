
from django.shortcuts import render,redirect




def home(request):
    if(request.method=='POST'):
        user=request.POST['username']
        return redirect(f'user/{user}')
    return render(request,'app/home.html')

def user(request,name):
    content={
        'name':name
    }
    return render(request,'app/index.html',{'content':content})


