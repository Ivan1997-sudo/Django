from rest_framework import serializers
from .models import Resume

class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        read_only_fields = ["user"]
        fields = ([
            "user",
            "position",
            "experience",
            "created_at"
        ])