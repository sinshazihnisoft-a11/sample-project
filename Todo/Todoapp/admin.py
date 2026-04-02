import re
from django import forms
from django.contrib import admin, messages

from .models import Todo_item, TodoComment

# Register your models here.
@admin.action(description='Mark selected items as completed')
def mark_as_completed(modeladmin, request, queryset):
    print('queryset1:', Todo_item.objects.all())
    print("queryset:", queryset)
    updated = queryset.update(is_completed=True)
    if updated :
        modeladmin.message_user(
            request,
            f"{updated} item(s) marked as completed.",
            messages.SUCCESS
        )
    else:
        modeladmin.message_user(
            request,
            "No items were marked as completed.",
            messages.WARNING
        )

@admin.action(description='Mark selected items as not completed')
def mark_as_not_completed(modeladmin, request, queryset):
    updated = queryset.update(is_completed=False)
    if updated :
        modeladmin.message_user(
            request,
            f"{updated} item(s) marked as not completed.",
            messages.SUCCESS
        )
    else:
        modeladmin.message_user(
            request,
            "No items were marked as not completed.",
            messages.WARNING
        )

class TodoCommentInline(admin.TabularInline):
    model = TodoComment
    extra = 1


class Todo_item_AdminForm(forms.ModelForm):
    class Meta:
        model = Todo_item
        fields = '__all__'

    def clean_name(self):
        name = self.cleaned_data.get("name")
        
        if not name:
            return name
        
        if len(name) < 3:
            raise forms.ValidationError("Name must be at least 3 characters long.")
        if not re.match("^[A-Za-z ]+$", name):
            raise forms.ValidationError("Name must contain only letters and spaces (no numbers or special charecter).")
        return name

class Todo_item_admin(admin.ModelAdmin):
    list_display = ('name', 'description', 'is_completed', 'created_at', 'created_by')
    list_filter = ('is_completed', 'created_at', 'created_by')
    search_fields = ('name', 'description', 'created_by__username')
    ordering = ('-created_at',)

    actions = [mark_as_completed, mark_as_not_completed]

    inlines = [TodoCommentInline]
    readonly_fields = ('created_at',)

    fieldsets = (
        ('Todo details', {
            'fields': ('name', 'description', 'is_completed')
        }),
        ('Audit info', {
            'fields': ('created_at', 'created_by'),
        }),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(created_by = request.user)
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

    def has_change_permission(self, request, obj=None):
        if obj is None:
            return True
        if request.user.is_superuser:
            return True
        return obj.created_by == request.user
    
    def has_delete_permission(self, request, obj=None):
        if obj is None:
            return True
        return request.user.is_superuser
    
    form = Todo_item_AdminForm
    

admin.site.register(Todo_item, Todo_item_admin)