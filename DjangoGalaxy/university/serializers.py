from rest_framework import serializers
from .models import University, Course, UniversityCourse


class UniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        read_only_fields = ["id"]
        fields = [
            "id",
            "name",
            "country"
        ]

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        read_only_fields = ["id"]
        fields = [
            "id",
            "title",
            "description"
        ]

class UniversityCourseSerializer(serializers.ModelSerializer):
    university = UniversitySerializer()
    course = CourseSerializer( )
    class Meta:
        model = UniversityCourse
        read_only_fields = ["id"]
        fields = [
            "id",
            "university",
            "course",
            "semester",
            "duration_weeks"
        ]

    def create(self, validated_data):
        university_data = validated_data.pop('university')
        course_data = validated_data.pop('course')
        university = University.objects.create(name=university_data['name'], country=university_data['country'])
        course = Course.objects.create(title=course_data['title'], description=course_data['description'])
        return super(UniversityCourseSerializer, self).create({
            "university": university,
            "course": course,
            **validated_data})

        # return UniversityCourse.objects.create(
        #     university=university,
        #     course=course,
        #     **validated_data)


class AllCoursesUniversity(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)
    class Meta:
        model = UniversityCourse
        fields = ["course", "semester", "duration_weeks"]

class CoursesUniversityStats(serializers.ModelSerializer):
    class Meta:
        model = UniversityCourse
        fields = ["duration_weeks"]