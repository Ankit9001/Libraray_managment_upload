import requests
from django.http import HttpResponse
from .models import Book, Member, Transaction
from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.db.models import Q
from django.shortcuts import get_object_or_404
from myapp.models import User


@login_required(login_url="/")
def get_book_data(request):
    api_url = "https://frappe.io/api/method/frappe-library?page=2&title=and"
    try:
        response = requests.get(api_url)
        data = response.json()
        print(data, "-------------")
        if "message" in data and data["message"]:
            print("in ifffffffff")
            for item in data["message"]:
                book_id = item.get("bookID")
                title = item.get("title")
                authors = item.get("authors")
                average_rating = item.get("average_rating")
                isbn = item.get("isbn")
                isbn13 = item.get("isbn13")
                language_code = item.get("language_code")
                pages = item.get("num_pages")
                rating_count = item.get("ratings_count")
                text_reviews_count = item.get("text_reviews_count")
                publication_date_str = item.get("publication_date")
                publisher = item.get("publisher")
                publication_date = datetime.strptime(publication_date_str, "%m/%d/%Y")

                formatted_publication_date = publication_date.strftime("%Y-%m-%d")
                book, created = Book.objects.update_or_create(
                    book_id=book_id,
                    defaults={
                        "title": title,
                        "author": authors,
                        "average_rating": average_rating,
                        "isbn": isbn,
                        "isbn13": isbn13,
                        "language_code": language_code,
                        "pages": pages,
                        "rating_count": rating_count,
                        "text_reviews_count": text_reviews_count,
                        "publication_date": formatted_publication_date,
                        "publisher": publisher,
                    },
                )
            return HttpResponse("Data successfully fetched and stored.")
        else:
            return HttpResponse("No results found in the API response.")
    except Exception as req_err:
        return HttpResponse(f"Request error: {str(req_err)}")


@login_required(login_url="/")
def home(request):
    data = Book.objects.filter(issue_book="n")
    return render(request, "homepage.html", {"data": data})


@login_required(login_url="/")
def book_delete(request, tid):
    data = Book.objects.filter(id=tid)
    data.delete()
    print("data deleted")
    return redirect("/home")


@login_required(login_url="/")
def add_book(request):
    if request.method == "POST":
        b_id = request.POST["b_id"]
        authorName = request.POST["authorName"]
        publisher = request.POST["publisher"]
        publication_date = request.POST["publication_date"]
        language = request.POST["language_code"]
        insert_data = Book.objects.create(
            book_id=b_id,
            author=authorName,
            publisher=publisher,
            publication_date=publication_date,
            language_code=language,
        )
        insert_data.save()
        print("data saved sucess")
        return redirect("/home")

    return render(request, "add.html")


@login_required(login_url="/")
def book_update(request, tid):
    if request.method == "POST":
        b_id = request.POST["b_id"]
        authorName = request.POST["authorName"]
        publisher = request.POST["publisher"]
        publication_date = request.POST["publication_date"]
        language = request.POST["language_code"]
        update_data = Book.objects.filter(id=tid)
        update_data.update(
            book_id=b_id,
            author=authorName,
            publisher=publisher,
            publication_date=publication_date,
            language_code=language,
        )
        print("data saved update")
        return redirect("/home")
    data = Book.objects.get(id=tid)
    content = {"data": data}
    return render(request, "update.html", content)


@login_required(login_url="/")
def search_data(request):
    query = request.GET.get("query")

    if query:
        books = Book.objects.filter(
            Q(author__icontains=query) | Q(publisher__icontains=query)
        )
    else:
        books = Book.objects.all()

    return render(request, "homepage.html", {"data": books, "query": query})


@login_required(login_url="/")
def book_detail_issue(request, pk):
    book = get_object_or_404(Book, pk=pk)
    members = Member.objects.all()
    if request.method == "POST":
        member_id = request.POST.get("member_dropdown")
        issue_date = request.POST.get("issue_date")
        return_date = request.POST.get("return_date")
        fee = request.POST.get("fee")
        member = get_object_or_404(Member, pk=member_id)
        if int(fee) > 0 and issue_date != "" and member_id != "" and return_date != "":
            total = member.outstanding_debt + int(fee)
            if total <= 500:
                print("in iffffffffffffffffffff")
                transaction = Transaction.objects.create(
                    book=book,
                    member=member,
                    issue_date=issue_date,
                    return_date=return_date,
                    fee=fee,
                )
                print(book.issue_book, "--------")
                book.issue_book = "y"
                print(book.issue_book, "=======")
                book.save()
                member.outstanding_debt += int(fee)
                member.save()
                print("transaction------created")
                return redirect("/home")
            else:
                print("in else")
                return HttpResponse("outstanding dept is graterthen 500")

    return render(request, "issuebook.html", {"data": book, "members": members})


def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if not username or not password:
            messages.error(request, "Please enter both username and password.")
            return render(request, "login.html")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/home")
        else:
            messages.error(request, "Invalid username or password.")
            return render(request, "login.html")
    return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect("/")


@login_required(login_url="/")
def update_user(request, tid):
    if request.method == "POST":
        name = request.POST["name"]
        location = request.POST["location"]
        update_data = Member.objects.filter(id=tid)
        update_data.update(name=name, location=location)
        return redirect("/home")
    else:
        data = User.objects.get(id=tid)
        context = {"data": data}
        return render(request, "updateregister.html", context)


@login_required(login_url="/")
def members(request):
    data = Member.objects.all()
    context = {"data": data}
    return render(request, "members.html", context)


@login_required(login_url="/")
def delete_member(request, tid):
    data = Member.objects.filter(id=tid)
    data.delete()
    return redirect("/members")


@login_required(login_url="/")
def update_member(request, tid):
    if request.method == "POST":
        name = request.POST["name"]
        location = request.POST["location"]
        update_data = Member.objects.filter(id=tid)
        update_data.update(name=name, location=location)
        print("data updated sucess")
        return redirect("/members")
    else:
        data = Member.objects.get(id=tid)
        context = {"data": data}
        return render(request, "update_member.html", context)


@login_required(login_url="/")
def user_register(request):
    print(request.user.id, "---------------")
    if request.method == "POST":
        name = request.POST["name"]
        location = request.POST["location"]
        print(name, "--", location, "c--")
        if name and location:
            print(request.user.id, "---------------")
            new_user = Member.objects.create(
                name=name, location=location, outstanding_debt=0
            )
            print("member created ")
            return redirect("/members")
    return render(request, "register.html")


def issue_book_detail(request):
    data = Transaction.objects.all()
    members = Member.objects.all()
    return render(request, "transaction.html", {"data": data, "members": members})


def return_book(request, pk):
    data = get_object_or_404(Book, pk=pk)
    data.is_return = "yes"
    data.issue_book = "n"
    data.save()
    fees_data=get_object_or_404(Member,)
    return redirect("/issue_book_detail")


