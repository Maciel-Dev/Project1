from django.http import response
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
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

            return render(request, "encyclopedia/pageAlreadyExists.html", {
                "titleExist": title
        })

        else:
            util.save_entry(title, content)

            search = util.get_entry(title)

            return render(request, "encyclopedia/pages.html", {   
                "names": mark.convert(search),
                "title": title
            })

    if title in util.list_entries():
        return render(request, "encyclopedia/pageAlreadyExists.html", {
            #Criar alert
        })

    return render(request, "encyclopedia/newPage.html")


def pageEdit(request, namePage):

    pageFile = open(f'entries\{namePage}.md', 'r+')
    reader = pageFile.read()
    pageFile.truncate(0)
    pageFile.close()
    pageFileAppend = open(f'entries\{namePage}.md', 'a', encoding="utf-8")
    content = request.GET.get('Body', '')
    appendThis = content
    pageFileAppend.write(appendThis)

    return render(request, "encyclopedia/pageEditTeste.html", {
        "textBody": reader,
        "page": namePage
    })

def randomPage(request):
    lista = util.list_entries()
    pageRandom = random.choice(lista)
    mark = markdown.Markdown()
    page = util.get_entry(pageRandom)

    return render(request, "encyclopedia/pages.html", {
        "names": mark.convert(page),
        "title": pageRandom
        
    })
