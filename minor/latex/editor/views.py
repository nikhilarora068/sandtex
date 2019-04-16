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
    context = {
    'instance': File.objects.all().filter(author=request.user)
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
    context = {
        'instance': objects,
        'files': files
    }

    return render(request, 'editor/file_detail.html', context)



@csrf_exempt
def save_content(request):
    if request.method == 'POST':
#        print(request.POST)
        if 'code' in request.POST:
            file_data = request.POST['code']

        if 'id' in request.POST:
            file_id = request.POST['id']
            instance  = File.objects.get(id=file_id)
            instance.content = file_data
            instance.save()

        if 'name' in request.POST:
            file_name = request.POST['name']
            File.objects.create(author=request.user, content=file_data, title=file_name)
            #print(f' id is = {file_id}')
            # pk = request.POST['pk']
            # print(f" pk = {pk}")
            #instance = File.objects.get(pk=pk)

            #print(instance.title)
#            print(f'file data = {file_data}')
            # doSomething with pieFact here...
        # print(f'file name is {file_name}')
        # if file_name == ""

        filename = os.path.join(settings.BASE_DIR, 'files')

        filename = filename + '/' + str(request.user) + '.tex'
        #print(f'filename is {filename}')

        with open(filename, 'w') as file:
            file.write(file_data)

        return HttpResponse('success') # if everything is OK
    # nothing went well
    return HttpResponse('FAIL!!!!!')



@csrf_exempt
def new_file_name(request):
    if request.method == 'POST':
        if 'name' in request.POST:
            filename = request.POST['name']
            default_content = "New file"
            instance = File.objects.create(title=filename, content=default_content, author=request.user)

            #print(filename)
        return HttpResponse('success')

    return HttpResponse('FAIL!!!!!')



@csrf_exempt
def delete_file(request):
    if request.method == 'POST':
        if 'id' in request.POST:
            file_id = request.POST['id']

            instance = File.objects.get(id = file_id)
            instance.delete()

            #print(filename)
        return HttpResponse('success')

    return HttpResponse('FAIL!!!!!')






@csrf_exempt
def compile(request):
    #os.system("pdflatex minor.tex")
    filename = os.path.join(settings.BASE_DIR, 'files')

    filename = filename + '/' + str(request.user) + '.tex'
    os.system("pdflatex -interaction=nonstopmode " + filename)
    # os.remove(str(request.user) + '.aux')
    # os.remove(str(request.user) + '.log')
    # os.remove('static/' + str(request.user) + '.pdf')
    # shutil.move(str(request.user) + '.pdf', 'static/')
    return HttpResponse('success')
