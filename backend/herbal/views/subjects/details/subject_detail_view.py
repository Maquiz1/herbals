from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q

from herbal.services.access_control import get_accessible_subjects
from herbal.models import Screening, VisitSchedule, CRF5
from herbal.models.queries.query_model import DataQuery


@login_required
def subject_detail_view(request, pk):

    # ---------------- ACCESS CONTROL ----------------
    subjects = get_accessible_subjects(request.user)

    subject = get_object_or_404(subjects, pk=pk)

    # ---------------- SCREENING + ENROLLMENT ----------------
    screening = (
        Screening.objects
        .select_related("enrollment")
        .filter(subject=subject)
        .first()
    )

    enrollment = screening.enrollment if screening else None

    # ---------------- VISITS ----------------
    visits = VisitSchedule.objects.none()

    if enrollment:
        visits = (
            VisitSchedule.objects
            .filter(enrollment=enrollment)
            .order_by("scheduled_date")
        )

    # ---------------- ADVERSE EVENTS ----------------
    adverse_events = CRF5.objects.none()

    if enrollment:
        adverse_events = (
            CRF5.objects
            .filter(enrollment=enrollment)
            .order_by("-event_date")
        )

    is_ltfu = False

    if enrollment and hasattr(enrollment, "termination"):
        is_ltfu = enrollment.termination.reason == "ltf"
    
    # ---------------- VISIT STATS (OPTIMIZED 🔥) ----------------
    visit_stats = visits.aggregate(
        total=Count("id"),
        completed=Count("id", filter=Q(status="completed"))
    )

    total_visits = visit_stats["total"]
    completed_visits = visit_stats["completed"]

    progress_percent = int((completed_visits / total_visits) * 100) if total_visits > 0 else 0

    # ---------------- QUERIES ----------------
    queries = DataQuery.objects.filter(visit__in=visits)

    # ---------------- CONTEXT ----------------
    context = {
        "subject": subject,
        "screening": screening,
        "enrollment": enrollment,
        "visits": visits,
        "adverse_events": adverse_events,
        "is_ltfu": is_ltfu,

        "completed_visits": completed_visits,
        "total_visits": total_visits,
        "progress_percent": progress_percent,

        "queries": queries,
    }

    return render(
        request,
        "herbal/subjects/subject_detail.html",
        context
    )