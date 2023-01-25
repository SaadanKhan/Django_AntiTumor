from django.shortcuts import redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView,FormView
from TODO_app.models import Task
from .models import Task
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


class CustomLogin(LoginView):
       template_name = 'TODO_app/login.html'
       fiels = '__all__'
       redirect_authenticated_user = True

       # Determine the URL to redirect to when the form is successfully validated. Returns success_url by default.
       def get_success_url(self):
              return reverse_lazy('TaskList')

class RegisterPage(FormView):
       template_name = 'TODO_app/register.html'
       form_class = UserCreationForm
       redirect_authenticated_user = True
       success_url = reverse_lazy('TaskList')

       def form_valid(self, form):
              user = form.save()
              if user is not None:
                     login(self.request, user)
              return super(RegisterPage,self).form_valid(form)

# This function will not bring the Logged in user to register page
       def get(self,*args, **kwargs):
              if self.request.user.is_authenticated:
                     return redirect('TaskList')
              return super(RegisterPage,self).get(*args, **kwargs)

# You can see that we have not rendered our class to task_list.html. 
# By default our class rendered towards the html file which is "prefix" of our class name.
# Although we can override them by our own defined template name...

# And also by default our class render the object_list, basiclly list of our object in model, to the template.
# So we don't need to send data of models manually in templates
# But if we want to override the name..!

class TaskList(LoginRequiredMixin , ListView):
       model = Task
       # Overriding the name from object_list to:
       context_object_name = 'tasks'
       
# By this function a user can only see his/her data
       def get_context_data(self, **kwargs):
              context = super().get_context_data(**kwargs) 
              context['tasks'] = context['tasks'].filter(user = self.request.user)
              context['count'] = context['tasks'].filter(complete = False).count()

              # getting the value from the "search-area"
              search_input = self.request.GET.get('search-area') or ''
              if search_input:
                    context['tasks'] = context['tasks'].filter(title__startswith=search_input) 

              context['search_input'] = search_input

              return context
       

# When we want to see the detail of the specific task
class TaskDetail(DetailView):
       model = Task
       context_object_name = 'detail'
       # overriding the template name
       template_name = 'TODO_app/detail.html'

class TaskCreate(LoginRequiredMixin , CreateView):
       model = Task
       # template_name = 'TODO_app/create.html'
       # Whenever we create task, it takes all the fields of the model Task and recreate them for the new purpose.
       fields = ['title','desc','complete']
       # To redirect the user after task create
       success_url = reverse_lazy('TaskList')

       def form_valid(self, form):
              form.instance.user = self.request.user
              return super(TaskCreate,self).form_valid(form)


class TaskUpdate(LoginRequiredMixin , UpdateView):
       model = Task
       # template_name = 'TODO_app/create.html'
       fields = ['title','desc','complete']
       # To redirect the user after task update
       success_url = reverse_lazy('TaskList')

class TaskDelete(LoginRequiredMixin , DeleteView):
       model = Task
       # template_name = 'TODO_app/del.html'
       context_object_name = 'task'
       success_url = reverse_lazy('TaskList')



