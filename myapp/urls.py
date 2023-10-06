from django.urls import path
from myapp import views

urlpatterns = [
    path("get_data/", views.get_book_data, name="get_book_data"),
    path("home/", views.home, name="home"),
    path("book_delete/<int:tid>", views.book_delete, name="book_delete"),
    path("add_data/", views.add_book, name="add_book"),
    path("book_update/<int:tid>", views.book_update, name="book_update"),
    path("search_data/", views.search_data, name="search_data"),
    path(
        "book_detail_issue/<int:pk>", views.book_detail_issue, name="book_detail_issue"
    ),
    path("", views.login_user, name="login_user"),
    path("logout_view/", views.logout_view, name="logout"),
    path("user_register/", views.user_register, name="user_register"),
    path("update_user/<int:tid>", views.update_user, name="update_user"),
    path("members/", views.members, name="members"),
    path("delete_member/<int:tid>", views.delete_member, name="delete_member"),
    path("update_member/<int:tid>", views.update_member, name="update_member"),
    path("issue_book_detail/", views.issue_book_detail, name="issue_book_detail"),
    path("return_book/<int:pk>", views.return_book, name="return_book"),
]
