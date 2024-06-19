from django import forms
from ToDoListApp.models import Task, Category

class TaskForm(forms.ModelForm):
    category_name = forms.CharField(max_length=100, label="Task Category")

    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'due_date', 'category_name']

    def clean_category_name(self):
        name = self.cleaned_data['category_name']
        return name