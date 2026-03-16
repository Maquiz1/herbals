from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from herbal.services.access_control import get_accessible_subjects
from herbal.models import Screening, VisitSchedule


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

    context = {
        "subject": subject,
        "screening": screening,
        "enrollment": enrollment,
        "visits": visits,
    }

    return render(
        request,
        "herbal/subjects/subject_detail.html",
        context
    )