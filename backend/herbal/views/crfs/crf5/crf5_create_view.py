from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from herbal.models import VisitSchedule
from herbal.forms.crfs.crf5_form import CRF5Form

@login_required
def crf5_create_view(request, pk):

    visit = get_object_or_404(VisitSchedule, pk=pk)

    if hasattr(visit, "crf5"):
        return redirect("herbal:subjects-detail", pk=visit.subject.pk)

    if request.method == "POST":

        form = CRF5Form(request.POST)

        if form.is_valid():

            crf = form.save(commit=False)

            crf.visit = visit

            crf.save()

            return redirect("herbal:subjects-detail", pk=visit.subject.pk)

    else:

        form = CRF5Form()

    return render(
        request,
        "herbal/crfs/crf5/crf5_form.html",
        {
            "form": form,
            "visit": visit
        }
    )