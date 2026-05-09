from django.shortcuts import render,redirect,get_object_or_404
from .models import Student,Marks


# Create your views here.
def home(request):
    search= request.GET.get('search')# search function ke liye
    students = Student.objects.all().order_by('roll_no')#all student ko call kar raha
    if search:
        students = Student.objects.filter(name__icontains=search) #name ke according search kar raha
    marks = Marks.objects.all()
    return render(request,'home.html',{'students':students})


def add(request):
    if request.method == 'POST': #post method use ho raha
        name = request.POST.get('name') #name le rahe hai
        roll_no = request.POST.get('roll_no')
        year = request.POST.get('year')

        Student.objects.create( #assign kar rahe
            name = name,
            roll_no = roll_no,
            year = year,
        )
        return redirect('/')
    return render(request,'add.html')
def delete(request,id):
    student = get_object_or_404(Student,id=id) #student ko la rahe hai
    student.delete() #elete kar rahe hai
    return redirect('/')

def edit(request,id):
    student = get_object_or_404(Student,id=id)
    if request.method == 'POST':
        student.name = request.POST.get('name')
        student.roll_no = request.POST.get('roll_no')
        student.year = request.POST.get('year')
        student.save()
        return redirect('/')
    return render(request,'edit.html',{'student':student})

def add_marks(request,id):
    student = get_object_or_404(Student,id=id)

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

def student_detail(request,id):
    student = get_object_or_404(Student,id=id)
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
