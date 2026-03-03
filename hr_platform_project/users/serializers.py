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
            delete_resume = Permission.objects.get(codename="delete_resume")
            view_resume = Permission.objects.get(codename="view_resume")
            respondents.permissions.set([add_resume, change_resume, view_resume])
            # Создаём группу "Администратор" и даём ей все разрешения
            admins = Group.objects.create(name="Администратор")
            admins.permissions.set([add_resume, change_resume, view_resume, delete_resume])
            # Создаём группу "HR-менеджер" и даём ей разрешение на просмотр резюме
            hr = Group.objects.create(name="HR-менеджер")
            hr.permissions.set([view_resume])
        user.groups.add(respondents)
        return user