from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from .models import User, Listing, Bids, WatchList, Comments, CATEGORIES
from django.db.models import Avg, Max, Min, Sum
class ListingNewPrice(forms.Form):
    bid = forms.IntegerField(label="Bid on this item")

class ListingCommentForm(forms.Form):
    comment = forms.CharField(label="Leave a comment")
CATEGORIES = (
    ("TOYS", "Toys"),
    ("FASHION", "Fashion"),
    ("ELECTRONICS", "Electronics"),
    ("SPORTS", "Sports"),
    ("HOME", "Home"),
    ("OTHER", "Other"),
)
class CreateListingForm(forms.Form):
    title = forms.CharField(label="Add a title for the listing")
    description = forms.CharField(label="Add a description")
    starting_bid = forms.IntegerField(label="Add an starting bid")
    URL_image = forms.URLField(initial='http://') 
    category = forms.ChoiceField(choices = CATEGORIES)

def listing(request, listing_id):
    listing=Listing.objects.get(id=listing_id)
    userr = request.user
    listingBids=listing.Bids.all()
    listingComments=listing.Comments.all()
    if listing.state==False:
        prices=listing.Bids.all().aggregate(Max('bid'))
        prices=prices["bid__max"]
        bidMax=listing.Bids.get(bid=prices)
    else:
        bidMax=[]
    if request.user.is_authenticated:
        listings=userr.WatchList.all()
    else:
        listings=[]
    if not listings:
        bandera="y"
        ws_id=0
    for ws in listings:
        if (ws.listings.title==listing.title):
            bandera="x"
            ws_id=ws.id
            print(ws_id,"WS_ID")
        else: 
            bandera="y"
            ws_id=0
            print(bandera,"BANDERA")
    if listing.user == userr:
        user_eq=True
    else:
        user_eq=False
    if request.method == "POST":
        if "comment" in request.POST:
            formComment = ListingCommentForm(request.POST)
            if formComment.is_valid():
                commentt=formComment.cleaned_data["comment"]
                p=Comments(listings=listing, user=userr, comment= commentt)
                p.save()
                return HttpResponseRedirect(reverse("index"))
            
            else: 
                return render(request, "auctions/listing.html", {
                    "listing": listing,
                    "currentPrice":maxlistingBid,
                    "formBid": formBid,
                    "formComment":formComment,
                    "message": "Your bid is less than other bids or greater than the starting bid",
                    "maxlistingBid":maxlistingBid,
                    "username":userr,
                    "bandera":bandera,
                    "ws_id":ws_id,
                    "user_eq": user_eq,
                    "bidMax":bidMax,
                    "listingComments":listingComments
                 })
            formBid = ListingNewPrice(request.POST)
        elif "bid" in request.POST:
            formBid=ListingNewPrice(request.POST)
            if formBid.is_valid():
                bidd = formBid.cleaned_data["bid"]
                if bidd >= listing.current_price and bidd >= listing.starting_bid:
                    p = Bids(Listing=listing, bid=bidd, user=userr)
                    listing.current_price=bidd
                    listing.save()
                    p.save()
                    return HttpResponseRedirect(reverse("index"))

                else: 
                    return render(request, "auctions/listing.html", {
                        "listing": listing,
                        "currentPrice":listing.current_price,
                        "formBid": formBid,
                        "formComment":ListingCommentForm(),
                        "message": "Your bid is less than other bids or greater than the starting bid",
                        "maxlistingBid":listing.current_price,
                        "username":userr,
                        "bandera":bandera,
                        "ws_id":ws_id,
                        "user_eq": user_eq,
                        "bidMax":bidMax,
                        "listingComments":listingComments
                    })
        else:
            return render(request, "auctions/listing.html", {
                "listing": listing,
                "formBid": formBid,
                "formComment":formComment,
                 "username":userr,
                 "bandera":bandera,
                 "ws_id":ws_id,
                 "user_eq": user_eq,
                 "bidMax":bidMax,
                 "listingComments":listingComments
            })
    else:
        
        return render(request, "auctions/listing.html", {
                "listing": listing,
                "formBid": ListingNewPrice(initial={'bid':listing.current_price} ),
                "formComment":ListingCommentForm(),
                "maxlistingBid":listing.current_price,
                 "username":userr,
                 "bandera":bandera,
                 "ws_id":ws_id,
                 "user_eq": user_eq,
                 "bidMax":bidMax,
                 "listingComments":listingComments
            })
    
def watchlist(request, username):
    if request.method == "POST":
        ws_id=request.POST.get("buttom")
        user=request.user.username
        userr=User.objects.get(username=user)
        listing=Listing.objects.get(id=ws_id)
        p=WatchList(listings=listing, user=userr)
        p.save()
        ws=userr.WatchList.all()
        if user==username:
            return render(request, "auctions/watchlist.html", {
               "listings": ws,
              })
        else:
            return render(request, "auctions/error.html", {
                "message": "Page not found"
                })
    else:
        user=request.user.username
        userr=User.objects.get(username=user)
        ws=userr.WatchList.all()
        if user==username:
            return render(request, "auctions/watchlist.html", {
                "listings": ws,
                })
        else:
            return render(request, "auctions/error.html", {
                "message": "Page not found"
                })
 
def createListing(request):
    if request.method == "POST":
        form = CreateListingForm(request.POST)
        userr = request.user
        if form.is_valid():
            titleForm = form.cleaned_data["title"]
            descriptionForm = form.cleaned_data["description"]
            starting_bidForm = form.cleaned_data["starting_bid"]
            URL_imageForm = form.cleaned_data["URL_image"]
            categoryForm = form.cleaned_data["category"]
            
            p = Listing(title=titleForm, description=descriptionForm, 
            starting_bid=starting_bidForm, URL_image=URL_imageForm, category=categoryForm, user=userr, current_price=starting_bidForm, state=True)
            p.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/createlisting.html", {
                "form": form
            })
    else:
        return render(request, "auctions/createlisting.html", {
            "form": CreateListingForm()
        })

def index(request):
    if request.method == "POST":
        ws_id=request.POST.get("deleteWL")
        userr = request.user
        ws=userr.WatchList.get(id=ws_id)
        ws.delete()
        listing=Listing.objects.all()
        bids=Bids.objects.all()
        
        return render(request, "auctions/index.html", {
            "listings": listing,
         })
    else:
        listing=Listing.objects.all()
        bids=Bids.objects.all()
        userr = request.user
        return render(request, "auctions/index.html", {
            "listings": listing,
            })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def closeListing(request, listing_id):
    listing=Listing.objects.get(id=listing_id)
    listingUs=listing.user
    username=request.user
    prices=listing.Bids.all().aggregate(Max('bid'))
    prices=prices["bid__max"]
    bidMax=listing.Bids.get(bid=prices)
    print(bidMax.user,"BIDMAX")
    if(username == listingUs):
        listing.state=False
        listing.save()
        return render(request, "auctions/success.html", {
           "message": "Your listing is now close",
           "bidMax":bidMax
         })
    else:
        return render(request, "auctions/error.html", {
            "message": "Not allow"
        })

def categories(request):
    listings=Listing.objects.values('category').distinct()
    L=[]
    for listing in listings:
        L.append(listing['category'])
    return render(request, "auctions/catindex.html", {
        "listings":L
    })
def category(request, listing_category):
    listing=Listing.objects.filter(category=listing_category)
    print(listing,"LISTING")
    return render(request, "auctions/categoryListing.html",{
        "listings":listing
    })