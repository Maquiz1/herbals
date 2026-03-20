from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Count, Sum

from herbal.models import Subject, Screening, Enrollment, VisitSchedule
from herbal.models.crfs.crf5.crf5_model import CRF5
from herbal.models import StudyTarget


@login_required
def dashboard_view(request):

    user = request.user
    profile = user.staff_profile
    role = profile.role

    subjects = Subject.objects.all()

    # 🔒 Role filtering
    if role in ["data_clerk", "coordinator"]:
        subjects = subjects.filter(site=profile.site)

    elif role in ["monitor", "reviewer", "pi"]:
        subjects = subjects.filter(site__in=profile.assigned_sites.all())

    screenings = Screening.objects.filter(subject__in=subjects)
    enrollments = Enrollment.objects.filter(screening__subject__in=subjects)
    visits = VisitSchedule.objects.filter(
        enrollment__screening__subject__in=subjects
    )

    today = timezone.now().date()

    # =========================
    # KPI
    # =========================
    total_subjects = subjects.count()
    screened_subjects = screenings.count()
    enrolled_subjects = enrollments.count()

    scheduled_visits = visits.count()
    completed_visits = visits.filter(status="completed").count()
    missed_visits = visits.filter(status="missed").count()

    overdue_visits = visits.filter(
        status="pending",
        scheduled_date__lt=today
    ).count()

    adverse_events = CRF5.objects.filter(
        enrollment__screening__subject__in=subjects
    ).count()

    # =========================
    # 🎯 OVERALL PROGRESS
    # =========================
    targets = StudyTarget.objects.all()

    # 🔒 Apply SAME role filtering
    if role in ["data_clerk", "coordinator"]:
        targets = targets.filter(site=profile.site)

    elif role in ["monitor", "reviewer", "pi"]:
        targets = targets.filter(site__in=profile.assigned_sites.all())

    total_target = targets.aggregate(
        total=Sum("target_enrollment")
    )["total"] or 0

    overall_percent = int((enrolled_subjects / total_target) * 100) if total_target > 0 else 0

    # =========================
    # 🏥 SITE PROGRESS
    # =========================
    site_progress = StudyTarget.objects.values(
        "site__name"
    ).annotate(
        target=Sum("target_enrollment"),
        enrolled=Count(
            "cancer_type__screening_cancer__enrollment",
            distinct=True
        )
    )

    # =========================
    # 🧬 CANCER PROGRESS
    # =========================
    cancer_progress = StudyTarget.objects.values(
        "cancer_type__name"
    ).annotate(
        target=Sum("target_enrollment"),
        enrolled=Count(
            "cancer_type__screening_cancer__enrollment",
            distinct=True
        )
    )

    # =========================
    # 🔬 SITE × CANCER
    # =========================
    detailed_progress = StudyTarget.objects.values(
        "site__name",
        "cancer_type__name",
        "target_enrollment"
    ).annotate(
        enrolled=Count(
            "cancer_type__screening_cancer__enrollment",
            distinct=True
        )
    )

    # =========================
    # % CALCULATIONS
    # =========================
    def add_percent(data, target_field):
        results = []
        for row in data:
            target = row.get(target_field, 0) or 0
            enrolled = row.get("enrolled", 0) or 0
            percent = int((enrolled / target) * 100) if target > 0 else 0

            row["percent"] = percent
            results.append(row)
        return results

    site_progress = add_percent(site_progress, "target")
    cancer_progress = add_percent(cancer_progress, "target")
    detailed_progress = add_percent(detailed_progress, "target_enrollment")

    # =========================
    # SITE SUMMARY
    # =========================
    site_summary = subjects.values("site__name").annotate(
        total=Count("id")
    )

    latest_subjects = subjects.select_related("site").order_by("-created_at")[:10]

    return render(request, "dashboard/dashboard.html", {
        "role": role,

        # KPI
        "total_subjects": total_subjects,
        "screened_subjects": screened_subjects,
        "enrolled_subjects": enrolled_subjects,

        # Visits
        "scheduled_visits": scheduled_visits,
        "completed_visits": completed_visits,
        "missed_visits": missed_visits,
        "overdue_visits": overdue_visits,

        # Safety
        "adverse_events": adverse_events,

        # Overall
        "total_target": total_target,
        "overall_percent": overall_percent,

        # Progress
        "site_progress": site_progress,
        "cancer_progress": cancer_progress,
        "detailed_progress": detailed_progress,

        # Other
        "site_summary": site_summary,
        "latest_subjects": latest_subjects,
    })