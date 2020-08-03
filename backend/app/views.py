
from django.shortcuts import render,redirect

from .models import User,JoinCode

from .hash import Hash


def home(request):
    if(request.method=='POST'):
        user=request.POST['username']
        return redirect(f'user/{user}')
    return render(request,'app/home.html')

def user(request,name):


    user_obj=User.objects.filter(name=name)
    

    if user_obj.exists():



        random_hash_obj=Hash(name)
        random_hash=random_hash_obj.get_hash()

        user_obj.update(joining_code=random_hash)
    
    else:
        random_hash_obj=Hash(name)
        random_hash=random_hash_obj.get_hash()
        user_obj=User.objects.create(name=name,joining_code=random_hash)
        user_obj.save()
        join_code_table=JoinCode.objects.create(creater=user_obj,joiner=user_obj)
        join_code_table.save()
        
 
    

    content={
        'name':name,
        'joining_code':random_hash
    }
    return render(request,'app/index.html',{'content':content})

    
def createroom(request,name):

    return redirect(f'/messages/user/{name}')

