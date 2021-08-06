from django.http import response
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
import markdown
from markdown.core import Markdown
from django.urls import reverse
from . import util
from django.http import HttpResponse
import os
from django.contrib import messages
import random


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry):
    mark = markdown.Markdown()
    page = util.get_entry(entry)
    if page is None:
        return render(request, "encyclopedia/error.html", {   
            "titleNotFound": entry
        })

    else:
        return render(request, "encyclopedia/pages.html", {   
            "names": mark.convert(page),
            "title": entry
        })

def search(request):
    mark = markdown.Markdown()
    value = request.GET.get('q', '')
    if util.get_entry(value) is not None:
        return render(request, "encyclopedia/pages.html", {
            "names": mark.convert(util.get_entry(value)),
            "title": value
        })

    else:
        listStrings = []
        for entry in util.list_entries():
            if value.lower() in entry.lower():
                listStrings.append(entry)

        if not listStrings:
                return render(request, "encyclopedia/noFound.html", {
                    "search": value
                })
        else:
            return render(request, "encyclopedia/searchResult.html", {
                "listStrings": listStrings
                    })
            

def newPage(request):
    title = request.GET.get('markDownTitle', '')
    content = request.GET.get('markDownBody', '')
    mark = markdown.Markdown()

    #Condition to check if there is a title and a content
    if title != "" and content != "":

        if title in util.list_entries():

            msg = f"Page with {title} already Created! Please, choose another title!"

            return render(request, "encyclopedia/newPage.html", {
                "error": msg
        })

        else:
            util.save_entry(title, content)

            search = util.get_entry(title)

            return render(request, "encyclopedia/pages.html", {   
                "names": mark.convert(search),
                "title": title
            })

    if title in util.list_entries():
        msg = "Mensagem de erro!"

        return render(request, "encyclopedia/newPage.html", {
            "error": msg
        })

    return render(request, "encyclopedia/newPage.html")


def pageEdit(request, namePage):

    reader = str("")

    if request.method == "GET":
        pageFile = open(f'entries/{namePage}.md', 'r+')
        reader = pageFile.read()
        pageFile.truncate(0)
        pageFile.close()
        pageFileWrite = open(f'entries/{namePage}.md', 'w')
        pageFileWrite.write(reader)
        pageFileWrite.close()
    
    elif request.method == "POST":
        #Talvez use reverse
        pageFile = open(f'entries/{namePage}.md', 'r+')
        reader = pageFile.read()
        pageFile.truncate(0)

        pageFileAppend = open(f'entries\{namePage}.md', 'a', encoding="utf-8")
        
        if request.POST.get('Body'):
            content = request.POST.get('Body')
            pageFileAppend.write(content)
            
            return HttpResponseRedirect(f"/wiki/{namePage}")


    return render(request, 'encyclopedia/pageEditTeste.html', {
        "textBody": reader,
        "page": namePage
    })


def randomPage(request):
    lista = util.list_entries()
    pageRandom = random.choice(lista)
    page = util.get_entry(pageRandom)
    mark = markdown.Markdown()

    return render(request, "encyclopedia/randomPage.html", {
        "names": mark.convert(page),
        "title": pageRandom
        
    })
