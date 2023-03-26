import random
from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound
from . import util
import markdown2

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    content = util.get_entry(title)
    if content is None:
        return HttpResponseNotFound("Requested page not found.")
    html_content = markdown2.markdown(content)
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": html_content
    })

def search(request):
    query = request.GET.get("q", "")
    entries = util.list_entries()
    if query in entries:
        return redirect("entry", title=query)
    matching_entries = [entry for entry in entries if query.lower() in entry.lower()]
    return render(request, "encyclopedia/search.html", {
        "query": query,
        "entries": matching_entries
    })

def create(request):
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]
        if util.get_entry(title) is not None:
            return HttpResponseNotFound("An entry with this title already exists.")
        util.save_entry(title, content)
        return redirect("entry", title=title)
    return render(request, "encyclopedia/create.html")

def edit(request, title):
    if request.method == "POST":
        content = request.POST["content"]
        util.save_entry(title, content)
        return redirect("entry", title=title)
    content = util.get_entry(title)
    if content is None:
        return HttpResponseNotFound("Requested page not found.")
    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "content": content
    })

def random_entry(request):
    entries = util.list_entries()
    random_title = random.choice(entries)
    return redirect("entry", title=random_title)
