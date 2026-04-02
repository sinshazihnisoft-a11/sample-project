from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Todo_item(models.Model):
    name = models.CharField(max_length= 100)
    description = models.TextField()
    is_completed = models.BooleanField(default= False)
    created_at = models.DateTimeField(auto_now_add= True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='todos')

    def clean(self):
        if not self.name:
            raise ValidationError("Name field cannot be empty.")
        if self.is_completed and not self.description:
            raise ValidationError("Completed items must have a description.")

    def __str__(self):
        return self.name
    
class TodoComment(models.Model):
    todo_item = models.ForeignKey(Todo_item, on_delete=models.CASCADE, related_name='comments')
    comment_text = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment on {self.todo_item.name} at {self.created_at}"