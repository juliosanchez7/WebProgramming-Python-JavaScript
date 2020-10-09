from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

CATEGORIES = (
    ("TOYS", "Toys"),
    ("FASHION", "Fashion"),
    ("ELECTRONICS", "Electronics"),
    ("SPORTS", "Sports"),
    ("HOME", "Home"),
    ("OTHER", "Other"),
)
class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=140)
    starting_bid = models.IntegerField()
    URL_image = models.URLField(max_length=300)
    category = models.CharField(max_length=11,
                  choices=CATEGORIES,
                  default="OTHER")
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name="Listing")
    current_price=models.IntegerField(blank=True)
    state=models.BooleanField()
    
    def __str__(self):
        return f"{self.id} {self.title} {self.description} {self.starting_bid} {self.URL_image} {self.category} {self.user} {self.state}"
class Bids(models.Model):
    Listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="Bids")
    bid=models.IntegerField()
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name="Bids")
    class Meta:
        get_latest_by = 'bid'
    def __str__(self):
        return f"{self.user} {self.bid}"

class Comments(models.Model):
    listings=models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="Comments")
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name="Comments")
    comment=models.CharField(max_length=140)
    def __str__(self):
        return f"{self.listings} {self.user} {self.comment}"
class WatchList(models.Model):
    listings=models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="WatchList")
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name="WatchList")
    def __str__(self):
        return f"{self.listings.title} {self.listings.description} {self.listings.current_price} {self.listings.URL_image}"




