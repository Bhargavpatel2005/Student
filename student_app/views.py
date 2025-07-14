from django.shortcuts import render, redirect, get_object_or_404
from .models import Student
from .forms import StudentForm
from django.contrib import messages
from django.http import HttpResponse
import csv
from django.db.models import Q
import io
from django.core.paginator import Paginator

def student_list(request):
    query = request.GET.get('search', '')
    students = Student.objects.filter(
        Q(name__icontains=query) | Q(email__icontains=query)
    ) if query else Student.objects.all()

    paginator = Paginator(students, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    if request.headers.get('HX-Request'):
        return render(request, 'student_table.html', {'page_obj': page_obj})

    return render(request, 'student_list.html', {'page_obj': page_obj, 'query': query})

def student_create(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Student added successfully.")
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'student_form.html', {'form': form})

def student_update(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, "Student updated successfully.")
            return redirect('student_list')
    else:
        form = StudentForm(instance=student)
    return render(request, 'student_form.html', {'form': form})

def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        messages.success(request, "Student deleted successfully.")
        return redirect('student_list')
    return render(request, 'student_confirm_delete.html', {'student': student})

def export_students_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=students.csv'

    writer = csv.writer(response)
    writer.writerow(['Name', 'Age', 'Email', 'Grade'])

    for student in Student.objects.all():
        writer.writerow([student.name, student.age, student.email, student.grade])

    return response

def import_csv(request):
    if request.method == 'POST':
        try:
            csv_file = request.FILES['csv_file']
            if not csv_file.name.endswith('.csv'):
                messages.error(request, 'Only CSV files are allowed.')
                return redirect('import_csv')
            decoded = csv_file.read().decode('utf-8')
            reader = csv.reader(io.StringIO(decoded))
            next(reader)
            for row in reader:
                Student.objects.create(name=row[0], age=row[1],email=row[2], grade=row[3])
            messages.success(request, 'Students imported successfully!')
            return redirect('student_list')
        except Exception as e:
            messages.error(request, f'Error: {e}')
            return redirect('import_csv')
    return render(request, 'import_csv.html')

def dashboard(request):
    total_students = Student.objects.count()
    return render(request, 'dashboard.html', {'total_students': total_students})
