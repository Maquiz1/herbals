from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from herbal.models import VisitSchedule
from herbal.forms.crfs.crf6_form import CRF6Form

@login_required
def crf6_create_view(request, pk):

    visit = get_object_or_404(VisitSchedule, pk=pk)

    if hasattr(visit, "crf6"):
        return redirect("herbal:subjects-detail", pk=visit.subject.pk)

    if visit.visit_day != "D0":
        return redirect("herbal:subjects-detail", pk=visit.subject.pk)

    if request.method == "POST":

        form = CRF6Form(request.POST)

        if form.is_valid():

            crf = form.save(commit=False)

            crf.visit = visit

            crf.save()

            return redirect("herbal:subjects-detail", pk=visit.subject.pk)

    else:

        form = CRF6Form()

    return render(
        request,
        "herbal/crfs/crf6/crf6_form.html",
        {
            "form": form,
            "visit": visit
        }
    )