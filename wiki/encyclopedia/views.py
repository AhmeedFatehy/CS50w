from markdown2 import Markdown
from random import randint
from django.contrib import messages
from django import forms
from django.urls import reverse
from django.http import Http404,HttpResponseRedirect
from django.shortcuts import render

from . import util


class query(forms.Form):
    q = forms.CharField()

class newEntry(forms.Form):
    title = forms.CharField(max_length=100, min_length=1, widget=forms.TextInput(attrs={
        'autocomplete': 'off',
        'autocapitalize': 'on'}))
    content = forms.CharField(widget=forms.Textarea(), max_length=2000, min_length=10)

m = messages

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

# Helper function to check if entry is found or not (handling lower case)
def check_entry(entry):
    page = util.get_entry(entry)
    if not page:
        # In case the entry was hardcoded in URL in lower case
        page = util.get_entry(entry.capitalize())
        if page:
            entry = entry.capitalize()
    return entry, page

def get_entry(request, entry):
    entry, page = check_entry(entry)
    
    if not page:
        # Entry not found
        return render(request, '404.html', {
            "entry" : entry
        })
    page = Markdown().convert(page)

    return render(request, 'encyclopedia/entry.html', {
        "content" : page,
        "entry" : entry
    })

def search_entry(request):
    if request.method == "POST":
        form = query(request.POST)
        if form.is_valid():
            q = form.cleaned_data["q"]
            q, page =  check_entry(q)
            # if the query found in enteries
            if page:
                return HttpResponseRedirect(f"/wiki/{q}")
        
            # check if the query is a substring from any entry
            entries = util.list_entries()
            matching_entries = []
            for entry in entries:
                if entry.lower().find(q.lower()) != -1:
                    matching_entries.append(entry)
            return render(request, 'encyclopedia/search.html', {
                "entries" : matching_entries
            })
        
def new(request):
    if request.method == "POST":
        form = newEntry(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            page = util.get_entry(title)
            if page:
                if not len(messages.get_messages(request)):
                    messages.add_message(request, messages.INFO, f"There is already an entry with the title ({title})!!!")
                m = messages.get_messages(request)
                return render(request, 'encyclopedia/new.html', {
                    'form' : form,
                    "messages": m
                })
            content = form.cleaned_data["content"]
            util.save_entry(title=title, content=content)
            return HttpResponseRedirect(reverse('get_entry', args=[title]))
            

    return render(request, 'encyclopedia/new.html', {
        'form' : newEntry()
    })

def edit(request, entry):
    if request.method == "POST":
        form = newEntry(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]            
            content = form.cleaned_data["content"]
            util.save_entry(title=title, content=content)
            return HttpResponseRedirect(f"/wiki/{title}")
    entry_content = util.get_entry(entry)
    intitial = {
        'title': entry,
        'content': entry_content
    }
    form = newEntry(initial=intitial)
    return render(request, 'encyclopedia/edit.html', {
        'form' : form,
        'entry' : entry
    })

def random(request):
    entries = util.list_entries()
    random_index = randint(0, len(entries)-1)
    random_entry = entries[random_index]
    return HttpResponseRedirect(reverse('get_entry', args=[random_entry]))