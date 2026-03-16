from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from herbal.models import Screening
from herbal.forms.screening_form import ScreeningForm


@login_required
def screening_update_view(request, pk):

    screening = get_object_or_404(Screening, pk=pk)

    subject = screening.subject

    if request.method == "POST":

        form = ScreeningForm(request.POST, instance=screening)

        if form.is_valid():
            form.save()

            return redirect(
                "herbal:subjects-detail",
                pk=subject.pk
            )

    else:

        form = ScreeningForm(instance=screening)

    return render(
        request,
        "herbal/screening/screening_form.html",
        {
            "form": form,
            "subject": subject,
            "is_update": True,
        }
    )