from django.db import models


class Course(models.Model):
    course_name = models.CharField(max_length=100)
    description = models.TextField()
    credits = models.IntegerField()

    class Meta:
        db_table = 'courses'

    def __str__(self):
        return self.course_name


class Student(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    birth_date = models.DateField()
    enrollment_date = models.DateField()

    class Meta:
        db_table = 'students'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class StudentCourse(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    grade = models.DecimalField(max_digits=3, decimal_places=2)
    enrollment_date = models.DateField()

    class Meta:
        db_table = 'student_courses'

    def __str__(self):
        return f"{self.student} - {self.course}"

class Department(models.Model):
    department_id = models.AutoField(primary_key=True)
    employee_count = models.IntegerField()
    manager = models.CharField(max_length=100)

    class Meta:
        db_table = "departments"
        managed = False


class Budget(models.Model):
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        db_column="department_id"
    )
    category = models.CharField(max_length=100, primary_key=True)
    planned_amount = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        db_table = "budget"
        managed = False