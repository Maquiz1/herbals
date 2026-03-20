from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from herbal.models import VisitSchedule
from herbal.forms.crfs.crf1_form import CRF1Form
from herbal.services.visit_completion import update_visit_status
from django.db import IntegrityError

from herbal.forms.crfs.crf1_other_medications_form import CRF1OtherMedicalFormSet

@login_required
def crf1_other_meication_form_view(request, pk):

    visit = get_object_or_404(VisitSchedule, pk=pk)

    if visit.visit_day != "D0":
        return redirect("herbal:subjects-detail", pk=visit.subject.pk)

    crf_instance = getattr(visit, "crf1", None)

    if request.method == "POST":
        form = CRF1Form(request.POST, instance=crf_instance)
        formset = CRF1OtherMedicalFormSet(request.POST, instance=crf_instance)

        if form.is_valid() and formset.is_valid():
            crf = form.save(commit=False)
            crf.visit = visit
            crf.save()

            formset.instance = crf
            formset.save()

            update_visit_status(visit)

            return redirect("herbal:subjects-detail", pk=visit.subject.pk)

    else:
        form = CRF1Form(instance=crf_instance)
        formset = CRF1OtherMedicalFormSet(instance=crf_instance)

    return render(
        request,
        "herbal/crfs/crf1/crf1_form.html",
        {
            "form": form,
            "formset": formset,
            "visit": visit,
            "is_update": crf_instance is not None
        }
    )