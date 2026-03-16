from herbal.models.visits.visit_schedule_model import VisitSchedule
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required


@login_required
def visit_mark_missed(request, pk):

    visit = get_object_or_404(VisitSchedule, pk=pk)

    if request.method == "POST":

        reason = request.POST.get("reason")

        visit.status = "missed"
        visit.missed_reason = reason
        visit.save()

        subject = visit.enrollment.screening.subject

        return redirect("herbal:subjects-detail", pk=subject.pk)

    return render(
        request,
        "herbal/visits/mark_missed.html",
        {"visit": visit}
    )