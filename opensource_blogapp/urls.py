from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("about/", views.aboutus, name="about"),
    path("contact/", views.contact, name="contact"),
    path("signup/", views.signup, name="signup"),
    path("signin/", views.signin, name="signin"),

    # blogs
    path("blogs/", views.blog_list, name="blog_list"),
    path("blogs/new/", views.blog_create, name="blog_create"),
    path("blogs/<slug:slug>/", views.blog_detail, name="blog_detail"),
    path("blogs/<slug:slug>/edit/", views.blog_edit, name="blog_edit"),
    path("blogs/<slug:slug>/delete/", views.blog_delete, name="blog_delete"),
    path("blogs/<slug:slug>/comment/", views.add_comment, name="add_comment"),
    path("blogs/<slug:slug>/like/", views.toggle_like, name="toggle_like"),
]
