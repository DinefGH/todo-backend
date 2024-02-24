import datetime
from rest_framework import serializers
from todolist.models import TodoItem


class TodoItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoItem
        fields = '__all__'
        read_only_fields = ('author',) 

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        validated_data['created_at'] = datetime.date.today()
        return super().create(validated_data)