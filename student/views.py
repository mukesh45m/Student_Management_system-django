from django.shortcuts import render,redirect,get_object_or_404
from .models import Student,Marks
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .forms import RegistrationForm



# Create your views here.
def main(request):
    return render(request,'base.html')

@login_required
def home(request):
    search= request.GET.get('search')# search function ke liye
    students = Student.objects.filter(user=request.user).order_by('roll_no')#all student ko call kar raha
    if search:
        students = Student.objects.filter(user=request.user,name__icontains=search) #name ke according search kar raha
    marks = Marks.objects.all()
    return render(request,'home.html',{'students':students})

@login_required
def add(request):
    if request.method == 'POST': #post method use ho raha
        name = request.POST.get('name') #name le rahe hai
        roll_no = request.POST.get('roll_no')
        year = request.POST.get('year')
        if Student.objects.filter(roll_no=roll_no).exists():
            messages.error(request,'Roll number already exists')
            return redirect('add')


        Student.objects.create( #assign kar rahe
            user = request.user,
            name = name,
            roll_no = roll_no,
            year = year,
        )
        return redirect('home')
    return render(request,'add.html')

@login_required
def delete(request,id):
    student = get_object_or_404(Student,id=id,user=request.user) #student ko la rahe hai
    student.delete() #elete kar rahe hai
    return redirect('home')

@login_required
def edit(request,id):
    student = get_object_or_404(Student,id=id,user=request.user)
    if request.method == 'POST':
        student.name = request.POST.get('name')
        student.roll_no = request.POST.get('roll_no')
        student.year = request.POST.get('year')
        student.save()
        return redirect('home')
    return render(request,'edit.html',{'student':student})

@login_required
def add_marks(request,id):
# def add_marks(request):
    student = get_object_or_404(Student,id=id,user=request.user)
    student = get_object_or_404(Student,user=request.user)

    # student =Student.objects.all()
    if request.method =='POST':
        # student_id = request.POST.get('student')
        subject = request.POST.get('subject')
        marks = request.POST.get('marks')
        # student = Student.objects.get(id = student_id)
        Marks.objects.create(
            student = student,
            subject=subject,
            marks = marks

        )
        return redirect(f'/student/{student.id}/')
    return render(request,'add_marks.html',{'students':student})

@login_required
def student_detail(request,id):
    student = get_object_or_404(Student,id=id,user=request.user)
    marks = Marks.objects.filter(student=student)
    total = 0
    for m in marks:
        total = total +m.marks
    percentage = 0
    if marks.count() >0:
        percentage = total/marks.count()
        percentage = round(percentage,2)
    context = {
        'student':student,
        'marks':marks,
        'total':total,
        'percentage':percentage
    }
    return render(request,'student_details.html',context)


def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            messages.success(request,'Registraion Success')
            return redirect('home')
        else:
            messages.error(request,'Registion Failed')
    else:
        form = RegistrationForm()
    return render(request,'signup.html',{'form':form})


def login_view(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,'Login Successful')
            return redirect('home')
        else:
            messages.error(request,'Invalid username or password')
    return render(request,'login.html')


    
def logout_view(request):
    logout(request)
    messages.success(request,'You have been logout')
    return redirect('main')
