import django.newforms as forms

from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User
from archweb_dev.main.utils import render_response
from archweb_dev.main.models import Todolist, TodolistPkg, Package
from archweb_dev.main.models import Arch, Repo

# FIXME: ugly hackery. http://code.djangoproject.com/ticket/3450
import django.db
IntegrityError = django.db.backend.Database.IntegrityError

class TodoListForm(forms.Form):
    name = forms.CharField(max_length=255,
            widget=forms.TextInput(attrs={'size': '30'}))
    description = forms.CharField(required=False,
            widget=forms.Textarea(attrs={'rows': '4', 'cols': '60'}))
    packages = forms.CharField(required=False,
            help_text='(one per line)',
            widget=forms.Textarea(attrs={'rows': '20', 'cols': '60'}))

    def clean_packages(self):
        packages = []
        for p in self.clean_data['packages'].split("\n"):
            for pkg in Package.objects.filter(
                    pkgname=p.strip()).order_by('arch').distinct():
                packages .append(pkg)

        return packages


def flag(request, listid, pkgid):
    list = get_object_or_404(Todolist, id=listid)
    pkg  = get_object_or_404(TodolistPkg, id=pkgid)
    pkg.complete = not pkg.complete
    pkg.save()
    return HttpResponseRedirect('/todo/%s/' % (listid))

def view(request, listid):
    list = get_object_or_404(Todolist, id=listid)
    return render_response(
        request, 
        'todolists/view.html', 
        {'list':list})

def list(request):
    lists = Todolist.objects.order_by('-date_added')
    for l in lists:
        l.complete = TodolistPkg.objects.filter(
            list=l.id,complete=False).count() == 0
    return render_response(request, 'todolists/list.html', {'lists':lists})

@permission_required('todolists.add_todolist')
def add(request):
    if request.POST:
        form = TodoListForm(request.POST)
        if form.is_valid():
            todo = Todolist.objects.create(
                creator     = request.user,
                name        = form.clean_data['name'],
                description = form.clean_data['description'])
            for pkg in form.clean_data['packages']:
                TodolistPkg.objects.create(list = todo, pkg = pkg)
            return HttpResponseRedirect('/todo/')
    else:
        form = TodoListForm()

    page_dict = {
            'title': 'Add To-do List',
            'form': form,
            'submit_text': 'Create List'
            }
    return render_response(request, 'general_form.html', page_dict)

@permission_required('todolists.change_todolist')
def edit(request, list_id):
    todo_list = get_object_or_404(Todolist, id=list_id)
    if request.POST:
        form = TodoListForm(request.POST)
        if form.is_valid():
            todo_list.name = form.clean_data['name']
            todo_list.description = form.clean_data['description']
            todo_list.save()

            packages = [p.pkg for p in todo_list.packages]

            for pkg in form.clean_data['packages']:
                if pkg not in packages:
                    TodolistPkg.objects.create(list = todo_list, pkg = pkg)

            return HttpResponseRedirect('/todo/%d/' % todo_list.id)
    else:
        form = TodoListForm(initial={
            'name': todo_list.name,
            'description': todo_list.description,
            'packages': todo_list.package_names,
            })
    page_dict = {
            'title': 'Edit To-do List "%s"' % todo_list.name,
            'form': form,
            'submit_text': 'Save List'
            }
    return render_response(request, 'general_form.html', page_dict)



# vim: set ts=4 sw=4 et:

