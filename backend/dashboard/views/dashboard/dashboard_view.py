# dashboard/views/dashboard_view.py

from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from herbal.models import Subject, Screening, Enrollment, VisitSchedule
from herbal.models.crfs.crf5.crf5_model import CRF5


@login_required
def dashboard_view(request):

    user = request.user
    profile = user.staff_profile
    role = profile.role

    subjects = Subject.objects.all()

    # Role based filtering
    if role in ["data_clerk", "coordinator"]:
        subjects = subjects.filter(site=profile.site)

    elif role in ["monitor", "reviewer", "pi"]:
        subjects = subjects.filter(site__in=profile.assigned_sites.all())

    # Screening
    screenings = Screening.objects.filter(subject__in=subjects)

    # Enrollment
    enrollments = Enrollment.objects.filter(
        screening__subject__in=subjects
    )

    # Visits
    visits = VisitSchedule.objects.filter(
        enrollment__screening__subject__in=subjects
    )

    today = timezone.now().date()

    # KPI counts
    total_subjects = subjects.count()
    screened_subjects = screenings.count()
    enrolled_subjects = enrollments.count()

    completed_visits = visits.filter(status="completed").count()
    missed_visits = visits.filter(status="missed").count()

    overdue_visits = visits.filter(
        status="pending",
        scheduled_date__lt=today
    ).count()

    adverse_events = CRF5.objects.filter(
        enrollment__screening__subject__in=subjects
    ).count()

    # Recruitment progress
    target_enrollment = settings.STUDY_TARGET_ENROLLMENT
    recruitment_percent = 0

    if target_enrollment > 0:
        recruitment_percent = int((enrolled_subjects / target_enrollment) * 100)

    context = {
        "role": role,

        "total_subjects": total_subjects,
        "screened_subjects": screened_subjects,
        "enrolled_subjects": enrolled_subjects,

        "completed_visits": completed_visits,
        "missed_visits": missed_visits,
        "overdue_visits": overdue_visits,

        "adverse_events": adverse_events,

        "target_enrollment": target_enrollment,
        "recruitment_percent": recruitment_percent,
    }

    return render(request, "dashboard/dashboard.html", context)