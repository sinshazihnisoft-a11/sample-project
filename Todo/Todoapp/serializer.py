from rest_framework import serializers

from Todoapp.models import Todo_item

class Todo_item_serializer(serializers.ModelSerializer): 
    class Meta:
        model = Todo_item
        fields = '__all__'

    def validate_name(self, value):
        if not value or value.strip() == "":
            raise serializers.ValidationError("Name field cannot be empty.")
        if len(value) < 3:
            raise serializers.ValidationError("Name must be at least 3 characters long.")
        return value
    
    def validate_description(self, value):
        if not value or value.strip() == "":
            raise serializers.ValidationError("Description field cannot be empty.")
        return value
    def validate(self, attr):
        is_completed = attr.get('is_completed', False)
        description = attr.get('description', '')

        if is_completed and not description:
            raise serializers.ValidationError("Completed items must have a description.")
        
        return attr
        