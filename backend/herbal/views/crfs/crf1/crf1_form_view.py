from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from herbal.models import VisitSchedule
from herbal.forms.crfs.crf1_form import CRF1Form
from herbal.services.visit_completion import update_visit_status
from django.db import IntegrityError


@login_required
def crf1_form_view(request, pk):

    visit = get_object_or_404(VisitSchedule, pk=pk)

    # Only allow Day 0
    if visit.visit_day != "D0":
        return redirect("herbal:subjects-detail", pk=visit.subject.pk)

    # Check if CRF already exists
    crf_instance = getattr(visit, "crf1", None)

    if request.method == "POST":
        form = CRF1Form(request.POST, instance=crf_instance)

        if form.is_valid():
            crf = form.save(commit=False)
            crf.visit = visit
            try:
                crf.save()
            except IntegrityError:
                form.add_error(None, "CRF1 already exists for this visit.")
                
            update_visit_status(visit)

            return redirect("herbal:subjects-detail", pk=visit.subject.pk)

    else:
        form = CRF1Form(instance=crf_instance)

    return render(
        request,
        "herbal/crfs/crf1/crf1_form.html",
        {
            "form": form,
            "visit": visit,
            "is_update": crf_instance is not None
        }
    )