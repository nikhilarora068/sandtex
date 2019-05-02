from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import File
import os
import shutil
from latex import settings





@login_required
def editor_window(request):
    all_user_files = File.objects.all().filter(author=request.user)
    no_of_files = len(all_user_files)

    context = {
        'count': no_of_files,
        'all_files': all_user_files
    }
    return render(request, 'editor/editor.html', context)




@login_required
def detail_view(request, pk=1):
    id = pk
    #print(id)
    files = File.objects.all().filter(author=request.user);
    objects = files.get(pk=id)
    #print(objects)
    #print(objects.content)
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    destination = os.path.join(BASE_DIR, "static")
    pdfname = str(request.user) + '.pdf'

    all_files = os.listdir(destination)

    if any(pdfname in s for s in all_files):
        file_status = 1
    else:
        file_status = 0

    # print(all_files)
    # print(pdfname)
    # print(file_status)


    destination = os.path.join(destination, pdfname)

    context = {
        'instance': objects,
        'files': files,
        'status': file_status
    }

    return render(request, 'editor/file_detail.html', context)


@login_required
@csrf_exempt
def sharing(request, pk=1):
    id = pk
    #print(id)
    files = File.objects.all().filter(author=request.user);
    objects = files.get(pk=id)
    #print(objects)
    #print(objects.content)
    context = {
        'instance': objects,
        'files': files
    }

    return render(request, 'share/sharing_window.html', context)





@csrf_exempt
def save_content(request):
    if request.method == 'POST':
#        print(request.POST)
        if 'code' in request.POST:
            file_data = request.POST['code']
            # print(file_data)

        if 'id' in request.POST:
            file_id = request.POST['id']
            instance  = File.objects.get(id=file_id)
            instance.content = file_data
            instance.save()
            # print(file_id)

        if 'name' in request.POST:
            file_name = request.POST['name']
            if file_name is not None and file_name is not "":
                File.objects.create(author=request.user, content=file_data, title=file_name)
            #print(f' id is = {file_id}')
            # pk = request.POST['pk']
            # print(f" pk = {pk}")
            #instance = File.objects.get(pk=pk)

            #print(instance.title)
            #print(f'file data = {file_data}')
            # doSomething with pieFact here...
        # print(f'file name is {file_name}')
        # if file_name == ""

        filename = os.path.join(settings.BASE_DIR, 'files')

        filename = filename + '/' + str(request.user) + '.tex'
        #print(f'filename is {filename}')

        with open(filename, 'w') as file:
            file.write(file_data)

        return HttpResponse('success')
        # new_file = File.objects.all().filter(author=request.user).order_by("-id")[0]
        # detail_view(request, new_file.id) # if everything is OK
    # nothing went well
    # return HttpResponse('FAIL!!!!!')



@csrf_exempt
def new_file_name(request):
    if request.method == 'POST':
        if 'name' in request.POST:
            filename = request.POST['name']
            if filename is not None and filename is not "":
                default_content = "New file"
                default_content = r''' \documentclass{article}
\usepackage[utf8]{inputenc}
\title{Galaxy}
\date{October 2018}
\usepackage{natbib}
\usepackage{graphicx}
\begin{document}
\maketitle
\section{Introduction}
There is a theory which states that if ever anyone discovers exactly what the Universe is for and why it is here, it will instantly dbizarre and inexplicable.
There is another theory which states that this has already happened.
nikhil
\section{Conclusion}
 "I always thought something was fundamentally wrong with the universe" \citep{adams1995hitchhiker}
\bibliographystyle{plain}
\bibliography{references}
\end{document}'''
                instance = File.objects.create(title=filename, content=default_content, author=request.user)

            #print(filename)
        return HttpResponse('success')

    # return HttpResponse('FAIL!!!!!')



@csrf_exempt
def delete_file(request):
    if request.method == 'POST':
        if 'id' in request.POST:
            file_id = request.POST['id']

            instance = File.objects.get(id = file_id)
            instance.delete()

            #print(filename)
        return HttpResponse('success')

    # return HttpResponse('FAIL!!!!!')






@csrf_exempt
def compile(request):
    #os.system("pdflatex minor.tex")
    filename = os.path.join(settings.BASE_DIR, 'files')

    filename = filename + '/' + str(request.user) + '.tex'
    os.system("pdflatex -interaction=nonstopmode " + filename)
    os.remove(str(request.user) + '.aux')
    os.remove(str(request.user) + '.log')
    # os.remove('static/' + str(request.user) + '.pdf')

    pdfname = str(request.user) + '.pdf'
    # BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # print(BASE_DIR)

    source = settings.BASE_DIR
    print(source)
    destination = os.path.join(settings.BASE_DIR, "static")
    print(destination)
    shutil.move(os.path.join(source, pdfname), os.path.join(destination, pdfname))
    #shutil.move(str(request.user) + '.pdf', 'static/')
    return HttpResponse('success')
