from django.shortcuts import render
from django.shortcuts import HttpResponse

from .forms import TaskForm
from .forms import AddTaskForm

from .utils import CURRENT_TASKS
from .utils import Task

# Create your views here.


def main(request):

    tasks = enumerate(CURRENT_TASKS, start=1)
    return render(request, 'main.html')


def add_task(request):
    if request.method == "POST":
        form = AddTaskForm(request.POST)
        if form.is_valid():

            t = Task()
            t.title = form.cleaned_data['title']
            t.estimate = form.cleaned_data['estimate']
            t.state = form.cleaned_data['state']

            CURRENT_TASKS.append(t)

            if t.is_critical():

                title_field = form.fields['title']
                title_field.widget.attrs['style'] = 'color:red'

            context = {
                'form': form,
                'hide': True,
                'success_msg': 'Task added successfully',
            }
        else:
            context = {
                'form': form,
                # 'hide': False,
            }
        return render(request, 'add_task.html', context)

    else:
        form = AddTaskForm()
        context = {
            'form': form,
            # 'hide': False,
        }
        return render(request, 'add_task.html', context)


def edit_task(request, ind):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():

            t = CURRENT_TASKS[int(ind)-1]
            t.title = form.cleaned_data['title']
            t.estimate = form.cleaned_data['estimate']
            t.state = form.cleaned_data['state']
            return HttpResponse('Task edited successfully')

    else:

        t = CURRENT_TASKS[int(ind)-1]

        fields = dict()
        fields['title'] = t.title
        fields['estimate'] = t.estimate
        fields['state'] = t.state

        form = TaskForm(data=fields)

        context = {
            'form': form,
        }

        return render(request, 'add_task.html', context)

