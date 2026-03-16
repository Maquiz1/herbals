from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from herbal.models.crfs.crf6.crf6_model import CRF6
from herbal.models import VisitSchedule
from herbal.forms.crfs.crf6_form import CRF6Form


@login_required
def crf6_update_view(request, pk):

    crf = get_object_or_404(CRF6, pk=pk)

    enrollment = crf.enrollment

    subject = enrollment.screening.subject

    if request.method == "POST":

        form = CRF6Form(request.POST, instance=crf)

        if form.is_valid():

            crf = form.save()

            # mark future visits N/A
            VisitSchedule.objects.filter(
                enrollment=enrollment,
                status="pending"
            ).update(status="na")

            return redirect(
                "herbal:subjects-detail",
                pk=subject.pk
            )

    else:

        form = CRF6Form(instance=crf)

    return render(
        request,
        "herbal/crfs/crf6/crf6_form.html",
        {
            "form": form,
            "crf": crf,
            "enrollment": enrollment,
            "subject": subject,
            "is_update": True,
        }
    )