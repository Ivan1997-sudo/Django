from rest_framework import serializers
from django.contrib.auth.models import User, Group, Permission

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ["username", "password"]

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
        )

        # Получаем или создаём группу
        respondents, created = Group.objects.get_or_create(name="Кандидат")
        if created:
            # Если группа только что создана — добавляем нужные разрешения
            add_resume = Permission.objects.get(codename="add_resume")
            change_resume = Permission.objects.get(codename="change_resume")
            view_resume = Permission.objects.get(codename="view_resume")
            respondents.permissions.set([add_resume, change_resume, view_resume])
        user.groups.add(respondents)
        return user