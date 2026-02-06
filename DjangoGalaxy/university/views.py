from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from .models import University, Course, UniversityCourse
from .serializers import UniversitySerializer, CourseSerializer, UniversityCourseSerializer, AllCoursesUniversity, CoursesUniversityStats
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend


class UniversityViewSet(ModelViewSet):
    queryset = University.objects.order_by("id")
    serializer_class = UniversitySerializer
    http_method_names = ["get", "delete", "post", "patch"]
    filter_backends = [SearchFilter]  # доступные действия
    search_fields = ["name"]  # поля для поиска

    @action(detail=True, methods=['get'], url_path="courses", url_name="university-course-all")
    def university_course_all(self, request, pk=None):
        university = self.get_object()
        uc = UniversityCourse.objects.filter(university=university)
        university_serializer = AllCoursesUniversity(uc, many=True)
        return Response({f"Университет {university.name}": [f"Курс: {i["course"]["title"]}, "
            f"семестр: {i['semester']}, продолжительность {i['duration_weeks']}"  for i in university_serializer.data]})

    @action(detail=True, methods=['get'], url_path="course-stats", url_name="university-course-stats")
    def university_course_stats(self, request, pk=None):
        university = self.get_object()
        uc = UniversityCourse.objects.filter(university=university)
        university_serializer = CoursesUniversityStats(uc, many=True)
        return Response({"total_courses": len(university_serializer.data),
            "average_duration": sum(i["duration_weeks"] for i in university_serializer.data)})


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    http_method_names = ["get", "delete", "post", "patch"]
    filter_backends = [DjangoFilterBackend, SearchFilter]  # доступные действия
    search_fields = ["title"]  # поля для поиска
    filterset_fields = {  # поля и суффиксы для фильтрации
        "title": ["exact", "contains"]
    }


class UniversityCourseViewSet(ModelViewSet):
    queryset = UniversityCourse.objects.all()
    serializer_class = UniversityCourseSerializer
    http_method_names = ["get", "delete", "post", "patch"]
    filter_backends = [DjangoFilterBackend, OrderingFilter]  # доступные действия
    ordering_fields = ["duration_weeks"]  # поля для сортировки
    filterset_fields = {  # поля и суффиксы для фильтрации
        "semester": ["exact"]
    }