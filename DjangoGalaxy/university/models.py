from django.db import models

class University (models.Model):
    name = models.CharField(max_length=50)
    country = models.CharField(max_length=50)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'country'], name='unique name and country')
        ]

    def __str__(self):
        return f'{self.name}, {self.country}'


class Course (models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['title', 'description'], name='unique title and description')
        ]

    def __str__(self):
        return f'{self.title}, {self.description}'


class UniversityCourse (models.Model):
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name="university")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="courses")
    semester = models.CharField(max_length=20)
    duration_weeks =  models.PositiveIntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['university', 'course', 'semester', 'duration_weeks'], name='unique university, course, name, semester and duration_weeks')
        ]

    def __str__(self):
        return f'{self.semester}: {self.duration_weeks}'