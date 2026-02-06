from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Question, Answer
from .serializers import QuestionSerializer, AnswerSerializer

class QuestionViewSet(ModelViewSet):
    queryset = Question.objects.order_by("-id")  # сортировка по -id для пагинации
    serializer_class = QuestionSerializer  #  сериализатор
    http_method_names = ["get", "delete", "post", "patch"]   # разрешенные методы
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]  # доступные действия
    search_fields = ["question_text", "choices__choice_text"]  # поля для поиска
    ordering_fields = ["pub_date"]  # поля для сортировки
    filterset_fields = {  # поля и суффиксы для фильтрации
        "id": ["in"],
        "question_text": ["exact", "contains"],
        "pub_date": ["gte", "lte"]
    }

    @action(detail=True, methods=['post'], url_path="answer",
            url_name="answer-question", serializer_class=AnswerSerializer)
    def answer_question(self, request, pk=None):
        answer_serializer = self.get_serializer(data=request.data)
        answer_serializer.is_valid(raise_exception=True)
        answer_data = answer_serializer.data
        question = self.get_object()
        Answer.objects.create(choice_id=answer_data["choice"], question=question)
        question_serializer = QuestionSerializer(question)
        return Response(question_serializer.data, status=201)