from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views


app_name = 'ToDoListApp'
urlpatterns = [
    path('admin/', admin.site.urls),
        # route is a string contains a URL pattern
    # view refers to the view function
    # name the URL
    path(route='', view=views.TaskListView.as_view(), name='index'),
    path('registration/', views.registration_request, name='registration'),
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_request, name='logout'),
    path('create/', views.create_task, name='create_task'),
    path('tasks/category/<str:category_name>/', views.TaskListByCategoryView.as_view(), name='tasks_by_category'),
    path('<uuid:pk>/', views.TaskDetailView.as_view(), name='task_details'),
    path('delete_task/<uuid:task_id>/', views.delete_task, name='delete_task'),
    path('update_task/<uuid:task_id>/', views.update_task, name='update_task'),

] # + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)