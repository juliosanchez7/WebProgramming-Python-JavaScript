from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("createlisting", views.createListing, name="createlisting"),
    path("register", views.register, name="register"),
    path("watchlist/<username>", views.watchlist, name="watchlist"),
    path("categories", views.categories, name="categories"),
    
    path("category/<listing_category>", views.category, name="category"),
    path("closeListing/<int:listing_id>", views.closeListing, name="closeListing")
]
