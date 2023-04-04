from django.shortcuts import render,redirect
from django.views import generic
from .models import *
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
# after account create the user will already logged in 
# Create your views here.

class CustomLoginView(LoginView):
    template_name='login.html'
    fields='__all__'
    redirect_authenticated_user=True
    
    def get_success_url(self):
        return reverse_lazy('tasks')

class RegisterPage(generic.FormView):
    template_name='todoapp/register.html'
    form_class=UserCreationForm
    #redirect authenticated user
    redirect_authenticated_user=True  
    success_url=reverse_lazy('tasks')


    def form_valid(self,form):
        user=form.save()
        if user is not None:
            login(self.request,user)
        return super(RegisterPage,self).form_valid(form)
    
    def get(self,*args,**kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage,self).get(*args,**kwargs)




class TaskList(LoginRequiredMixin,generic.ListView):
    model=Task
    context_object_name='tasks'
# used for user can only see their data
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context['tasks']=context['tasks'].filter(user=self.request.user)
        context['count']=context['tasks'].filter(complete=False).count()
        search_input=self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks']=context['tasks'].filter(title__startswith=search_input)
            context['search_input']=search_input
        return context

class TaskDetail(LoginRequiredMixin,generic.DetailView):
    model=Task
    context_object_name='task'
    template_name='todoapp/task.html'

class TaskCreate(LoginRequiredMixin,generic.CreateView):
    model=Task
    fields=['title','description','complete']
    success_url=reverse_lazy('tasks')

    def form_valid(self,form):
        form.instance.user=self.request.user
        return super(TaskCreate,self).form_valid(form)

class TaskUpdate(LoginRequiredMixin,generic.UpdateView):
    model=Task
    fields=['title','description','complete']
    success_url=reverse_lazy('tasks')

class DeleteView(LoginRequiredMixin,generic.DeleteView):
    model=Task
    context_object_name="task"
    success_url=reverse_lazy('tasks')




