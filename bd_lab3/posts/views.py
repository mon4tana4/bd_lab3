from django.db.models import Avg, Min, Max, Count, Sum
from django.db.models.functions import ExtractYear
from django.shortcuts import render
from .models import *


def get_university_data(db, request):
    course_id = request.GET.get("course_id")
    student_id = request.GET.get("student_id")

    data = {
        "courses": Course.objects.using(db).all(),
        "students": Student.objects.using(db).all(),
        "enrollments": StudentCourse.objects.using(db).select_related("student", "course"),

        "olap_courses": StudentCourse.objects.using(db).values(
            "course__course_name"
        ).annotate(
            avg=Avg("grade"),
            min=Min("grade"),
            max=Max("grade"),
            count=Count("student")
        ),

        "olap_students": StudentCourse.objects.using(db).values(
            "student__first_name", "student__last_name"
        ).annotate(
            avg=Avg("grade"),
            count=Count("course")
        ),

        "olap_years": StudentCourse.objects.using(db).annotate(
            year=ExtractYear("enrollment_date")
        ).values("year").annotate(
            avg=Avg("grade"),
            count=Count("student")
        ),

        "cube": StudentCourse.objects.using(db).select_related("student", "course"),
    }

    if course_id:
        data["slice_course"] = StudentCourse.objects.using(db).filter(
            course_id=course_id
        ).select_related("student")

    if student_id:
        data["slice_student"] = StudentCourse.objects.using(db).filter(
            student_id=student_id
        ).select_related("course")

    return data


def get_accounting_data(db):
    return {
        "departments": Department.objects.using(db).all(),
        "budgets": Budget.objects.using(db).select_related("department"),

        "budget_by_department": Budget.objects.using(db).values(
            "department__department_id"
        ).annotate(
            total=Sum("planned_amount"),
            avg=Avg("planned_amount"),
            count=Count("category")
        ),

        "budget_by_category": Budget.objects.using(db).values(
            "category"
        ).annotate(
            total=Sum("planned_amount"),
            avg=Avg("planned_amount"),
            count=Count("department")
        ),

        "budget_by_manager": Budget.objects.using(db).values(
            "department__manager"
        ).annotate(
            total=Sum("planned_amount"),
            count=Count("category")
        ),
    }

def dashboard(request):
    db = request.GET.get("db", "default")
    section = request.GET.get("section", "courses")

    context = {
        "db": db,
        "section": section
    }

    if db == "accounting":
        context.update(get_accounting_data(db))
    else:
        context.update(get_university_data(db, request))

    return render(request, "dashboard.html", context)