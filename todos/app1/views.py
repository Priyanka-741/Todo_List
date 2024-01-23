from django.shortcuts import redirect, render,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from app1.forms import TODOform
from app1.models import TODO
from django.contrib.auth.decorators import login_required

def display(request):
    return render(request, 'index.html')

def user_login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        unm = request.POST['uname']
        upass = request.POST['pass']
        user = authenticate(request, username=unm, password=upass)
        if user is not None:
            login(request, user)
            return redirect('/')  # Authentication successful
        else:
            return redirect('/login')  # Authentication failed

def user_signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html')
    else:
        nm = request.POST['fname']
        username = request.POST['uname']
        upass = request.POST['pass']
        obj = User.objects.create_user(username=username, first_name=nm, password=upass)
        obj.save()
        return redirect("/")

@login_required(login_url='login') #returns login page until n unless we are logged in
def home(request):
    if request.user.is_authenticated:
        user = request.user
        form=TODOform()
        todos=TODO.objects.filter(user=user).order_by('priority')
        return render(request,'index.html',context={'form':form, 'todos':todos})

@login_required(login_url='login')
def add_todo(request):
    if request.user.is_authenticated:
        user = request.user
        form = TODOform(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = user
            todo.save()
            print("Todo added:", form.cleaned_data)
            return redirect("/")
        else:
            return render(request, 'index.html', context={'form': form})
        
def signout(request):
    logout(request)
    return redirect("login")

def delete_todo(request,id):
    print(id)
    TODO.objects.get(pk=id).delete()
    return redirect("home")

def change_todo(request,id,status):
    todo=TODO.objects.get(pk=id)
    todo.status=status
    todo.save()
    return redirect("home")

@login_required(login_url='login')
def update_todo(request,id):
    if request.user.is_authenticated:
        user=request.user
        todo = get_object_or_404(TODO, pk=id, user=user)

        if request.method=='POST':
            form=TODOform(request.POST,instance=todo)
            if form.is_valid():
                form.save()
                return redirect("home")
            else:
                return render(request,'update_todo.html',context={'form':form,'todo':todo})
        else:
            form = TODOform(instance=todo)
            return render(request, 'update_todo.html', context={'form': form, 'todo': todo})
    else:
        return redirect('index.html')

    

