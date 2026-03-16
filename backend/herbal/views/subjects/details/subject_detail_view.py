from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from herbal.services.access_control import get_accessible_subjects
from herbal.models import Screening, VisitSchedule,CRF5
from herbal.models.queries.query_model import DataQuery

@login_required
def subject_detail_view(request, pk):

    subjects = get_accessible_subjects(request.user)

    subject = get_object_or_404(subjects, pk=pk)

    screening = Screening.objects.filter(subject=subject).first()

    enrollment = None
    visits = None

    if screening:
        enrollment = getattr(screening, "enrollment", None)

    if enrollment:
        visits = VisitSchedule.objects.filter(
            enrollment=enrollment
        ).order_by("scheduled_date")

    adverse_events = None

    if enrollment:
        adverse_events = CRF5.objects.filter(
            enrollment=enrollment
        ).order_by("-event_date")
    
    
    completed_visits = 0
    total_visits = 0

    if visits:

        total_visits = visits.count()

        completed_visits = visits.filter(status="completed").count()

    progress_percent = 0

    if total_visits > 0:
        progress_percent = int((completed_visits / total_visits) * 100)
    
    
    queries = DataQuery.objects.filter(
        visit__in=visits
    )
    context = {
        "subject": subject,
        "screening": screening,
        "enrollment": enrollment,
        "visits": visits,
        "adverse_events":adverse_events,
        
        
        
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