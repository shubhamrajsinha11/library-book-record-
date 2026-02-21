from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import admin
from django.shortcuts import render,redirect
from django.shortcuts import get_object_or_404
from .models import student
from .models import books
from .models import Rental
from django.http import JsonResponse


def home(request):
    return render(request,"home.html",context={"current_tab": "home"})

def save_student(request):
    if request.method == "POST":
        student_item = student(
            student_name=request.POST['student_name'],
            student_contact=request.POST['student_contact'],
            student_id=request.POST['student_id'],
            student_address=request.POST['address'],
            active=True
        )
        student_item.save()
        return redirect('/readers')
    return redirect('/')

def students_tab(request):
    if request.method=="GET":
        students = student.objects.all()
        return render(request,"readers.html",
                      context={"current_tab": "students",
                                                      "students":students}
                      )
    else:
        query = request.POST['query']
        students = student.objects.filter(student_name__icontains=query)
        return render(request, "readers.html",
                      context={"current_tab": "students",
                               "students": students,"query":query}
                      )

def books_tab(request):
    if request.method == "GET":
        book_list = books.objects.all()
    else:
        query = request.POST.get('query', '')
        book_list = books.objects.filter(book_name__icontains=query)

    return render(request, "books.html", {
        "current_tab": "book",
        "book": book_list,
        "bag_ids": request.session.get('bag', []),
        "query": request.POST.get('query', '') if request.method != "GET" else ''

    })

def toggle_bag(request, book_id):
    bag = request.session.get('bag', [])

    try:
        book_id = int(book_id)
    except (ValueError, TypeError):
        print("ERROR: Invalid book ID passed to toggle_bag")
        return redirect("books_tab")

    if book_id in bag:
        bag.remove(book_id)
    else:
        bag.append(book_id)

    request.session['bag'] = bag
    print("BAG AFTER TOGGLE:", bag)

    return redirect("books_tab")



def bag_view(request):
    bag_ids = request.session.get('bag', [])

    print("DEBUG: Raw Bag contains:", bag_ids)

    try:
        bag_ids = [int(id) for id in bag_ids if str(id).isdigit()]
    except Exception as e:
        print("ERROR: Could not convert bag_ids to integers:", e)
        bag_ids = []

    print("DEBUG: Clean Bag IDs:", bag_ids)

    bag_books = books.objects.filter(id__in=bag_ids)
    all_students = student.objects.all()

    return render(request, 'bag.html', {
        'bag': bag_books,
        'students': all_students,
        "current_tab": "bag"
    })

def clear_bag(request):
    request.session['bag'] = []
    return redirect('books_tab')



def bag_list(request):
    if request.method == "GET":
        students = student.objects.all()
    else:
        query = request.POST.get('query', '')
        students = student.objects.filter(student_name__icontains=query)

    return render(request, "bag.html", {
        "current_tab": "bag",
        "students": students,
        "query": request.POST.get('query', '') if request.method != "GET" else ''
    })

def get_student_details(request):
    ref_id = request.GET.get('ref_id')
    try:
        stud = student.objects.get(student_ref_id=ref_id)
        data = {
            'name': stud.student_name,
            'contact': stud.student_contact,
            'student_id': stud.student_id,
        }
        return JsonResponse(data)
    except student.DoesNotExist:
        return JsonResponse({'error': 'Student not found'}, status=404)


def checkout(request):
    if request.method == 'POST':
        ref_id = request.POST.get('student_ref_id')
        name = request.POST.get('student_name')
        contact = request.POST.get('student_contact')
        student_id = request.POST.get('student_id')
        start_date = request.POST.get('start_date')
        return_date = request.POST.get('return_date')
        bag = request.session.get('bag', [])

        for book_id in bag:
            book = books.objects.get(id=book_id)
            Rental.objects.create(
                student_ref_id=ref_id,
                student_name=name,
                student_contact=contact,
                student_id=student_id,
                book_name=book.book_name,
                rental_date=start_date,
                return_date=return_date
            )

        request.session['bag'] = []  # Clear bag after checkout
        return redirect('returns')  # Go to returns page

    return redirect('home')

def returns(request):
    query = request.GET.get('query', '')
    if query:
        rentals = Rental.objects.filter(student_name__icontains=query)
    else:
        rentals = Rental.objects.all()
    return render(request, 'returns.html', {'returns': rentals, 'query': query})

def toggle_return(request, rental_id):
    rental = get_object_or_404(Rental, id=rental_id)
    rental.delete()
    return redirect('returns')




