from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from herbal.models import VisitSchedule
from herbal.forms.crfs.crf1_form import CRF1Form
from herbal.services.visit_completion import update_visit_status
from django.db import IntegrityError
from herbal.forms.crfs.crf1_other_medications_form import CRF1OtherMedicalFormSet
from herbal.forms.crfs.crf1_nimregenin_form import CRF1NimregeninFormSet
from herbal.forms.crfs.crf1_other_herbal_form import CRF1OtherHerbalFormSet

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
        formset = CRF1OtherMedicalFormSet(
            request.POST,
            instance=crf_instance,
            prefix="othermedicals"
        )
        nim_formset = CRF1NimregeninFormSet(
            request.POST,
            instance=crf_instance,
            prefix="nimregenins"
        )

        herbal_formset = CRF1OtherHerbalFormSet(
            request.POST,
            instance=crf_instance,
            prefix="otherherbals"
        )
        
        if form.is_valid() and formset.is_valid() and nim_formset.is_valid() and herbal_formset.is_valid():
            crf = form.save(commit=False)
            crf.visit = visit

            try:
                crf.save()

                formset.instance = crf
                nim_formset.instance = crf
                herbal_formset.instance = crf

                formset.save()
                nim_formset.save()
                herbal_formset.save()

                update_visit_status(visit)

                return redirect("herbal:subjects-detail", pk=visit.subject.pk)

            except IntegrityError:
                form.add_error(None, "CRF1 already exists for this visit.")

    else:
        form = CRF1Form(instance=crf_instance)
        formset = CRF1OtherMedicalFormSet(
            instance=crf_instance,
            prefix="othermedicals"   # ✅ ADD THIS
        )
        nim_formset = CRF1NimregeninFormSet(
            instance=crf_instance,
            prefix="nimregenins"
        )
        herbal_formset = CRF1OtherHerbalFormSet(
            instance=crf_instance,
            prefix="otherherbals"
        )

    return render(
        request,
        "herbal/crfs/crf1/crf1_form.html",
        {
            "form": form,
            "formset": formset,
            "nim_formset": nim_formset,
            "herbal_formset": herbal_formset,
            "visit": visit,
            "is_update": crf_instance is not None
        }
    )