from rest_framework import viewsets
from .models import Resume
from .serializers import ResumeSerializer
from .permissions import ResumePermission

class ResumeViewSet(viewsets.ModelViewSet):
    permission_classes = [ResumePermission]  # разрешение на CRUD-операции
    queryset = Resume.objects.none()
    serializer_class = ResumeSerializer
    http_method_names = ["get", "delete", "post", "patch"]  # разрешенные методы

    #При создании резюме передает id пользователя в таблицу
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name="Кандидат").exists():
            return Resume.objects.filter(user=user)
        return Resume.objects.all()