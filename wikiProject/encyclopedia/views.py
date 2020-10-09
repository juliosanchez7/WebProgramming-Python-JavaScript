from django.shortcuts import render
from django.http import HttpResponse
import markdown2
import random
from django import forms
from . import util
from django.urls import reverse
from django.http import HttpResponseRedirect

#Create forms
class NewPageForm(forms.Form):
    title = forms.CharField(label="Title of the page")
    Content= forms.CharField(widget=forms.Textarea)


class EditPageForm(forms.Form):
    title = forms.CharField(label="Title of the page")
    Content= forms.CharField(widget=forms.Textarea)
    

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
#Newpage function, display a black form with textarea to create a new .md file
def newpage(request): 
    print("ESTOY AQAA")
    #Validations of the form
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            titlepage = form.cleaned_data["title"]
            contentpage = form.cleaned_data["Content"]
            #validation if the title already exist
            if util.get_entry(titlepage) is None:
                #save new .md file
                util.save_entry(titlepage, contentpage)
                return HttpResponseRedirect(reverse("index"))
            else: 
                return render(request, "encyclopedia/error.html", {
                    "message": "This documment already exists, try to change the title."
                     })
        else:
            return render(request, "encyclopedia/newpage.html", {
                    "form": form
                })
    else:
        return render(request, "encyclopedia/newpage.html", {
            "form":NewPageForm()
        })
#Edit function, display an editable version of a page in a  pre-populated textarea 

def edit(request, title):
    #Get the content of the .md file
    content=util.get_entry(title)
    if request.method == "POST":
        form = EditPageForm(request.POST)
        #validations of the form
        if form.is_valid():
            titlepage = form.cleaned_data["title"]
            contentpage = form.cleaned_data["Content"]
            #overwrite the .md file
            util.save_entry(titlepage, contentpage)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "encyclopedia/edit.html", {
                "form": form
                    })
    else:
        return render(request, "encyclopedia/edit.html", {
            "form": EditPageForm(initial={'title': title, 'Content': content})
        })
#random function, display a random page
def randompage(request):
    #list the .md files
    titles=util.list_entries()
    #take the lenght of the titles list
    length=len(titles)-1
    #generate a random function between 0 and lenght list -1 
    randomNum=random.randint(0, length)
    #displays a random title
    title=titles[randomNum]
    titlee=util.get_entry(title)
    content=markdown2.markdown(titlee)
    return render(request, "encyclopedia/titles.html", {
        "title": title.capitalize(),
        "content": content
    }) 
#funtion that alows to search with the form or with url "wiki/titleName"
def TITLE(request, title):
    titlee=util.get_entry(title)
    #if the search is by form:
    if request.method == 'GET':
        #get q value of the form.
        query= request.GET.get('q')
        if query is not None:
            titles=util.list_entries()
            #make a search between q value and titles created before.
            matching = [s for s in titles if query in s]
            #if the match is empty:
            if matching == []:
                return render(request, "encyclopedia/error.html", {
                    "message": "Your search does not have results"
                })
            #If appears a match: list the matching results.
            else:
                return render(request, "encyclopedia/search.html", {
                "entries": matching
                })
    #search via URL: be sure that the title exist.
    if titlee is not None:
        content=markdown2.markdown(titlee)
        #return a render with the title.
        return render(request, "encyclopedia/titles.html", {
            "title": title.capitalize(),
            "content": content
        })
    #If the "Wiki/TitleName" does not exist, display an error page.
    else :
        return render(request, "encyclopedia/error.html", {
                    "message": "Your request page was not found"
                })  


