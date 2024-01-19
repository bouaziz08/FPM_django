from datetime import timezone

from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth import login
from django.core.mail import send_mail
from .forms import UserRegistrationForm
from .models import Task

# Create your views here.


class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')

def logout_user(request):
    logout(request)
    return redirect('tasks')

class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('tasks')  # Update with your success page URL

    def form_valid(self, form):
        form.save()  # This saves the user to the database
        # Add any additional logic or redirects as needed
        return super().form_valid(form)

# class RegisterPage(FormView):
#     template_name = 'base/register.html'
#     form_class = UserCreationForm
#     redirect_authenticated_user = True
#     success_url = reverse_lazy('tasks')
#
#     def form_valid(self, form):
#         user = form.save()
#         if user is not None:
#             login(self.request, user)
#         return super(RegisterPage, self).form_valid(form)
#
#     def get(self, *args, **kwargs):
#         if self.request.user.is_authenticated:
#             return redirect('tasks')
#         return super(RegisterPage, self).get(*args, **kwargs)


class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(title__startswith=search_input)

        context['search_input'] = search_input

        return context


class TaskDetails(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'base/task.html'

class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'priority', 'deadline', 'complete']
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'deadline', 'complete']
    success_url = reverse_lazy('tasks')

class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')

class TaskConfirm(View):
    # model = Task
    # fields = ['complete']
    # success_url = reverse_lazy('tasks')

    def get(self, request, *args, **kwargs):
        task_id = kwargs['pk']
        task = Task.objects.get(pk=task_id)
        task.complete = True
        sendemail(task.id)
        task.save()
        return redirect('tasks')

# def Sendmail(id):
#     send_mail(
#         'Subject',
#         'Message body',
#         'djangopfm@gmail.com',
#         ['bouaziz.design08@gmail.com'],
#         fail_silently=False,
#     )

def sendemail(task_id):
     task = Task.objects.get(pk=task_id)
     user = task.user.username
     email = render_to_string('base/email.html', {'recipient': user, 'task_title': task.title})
     subject = f"Bravo pour l'achèvement réussi de la tâche !: {task.title}"
     message = email
     html_message = email
     from_email = "djangopfm@gmail.com"  # Update with your email
     recipient_list = [task.user.email]  # Update with the assignee's email
     send_mail(subject, message, from_email, recipient_list, html_message=email)

