from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from herbal.models import Subject, Enrollment
from herbal.forms.enrollment_form import EnrollmentForm
from herbal.services.visit_scheduler import generate_visit_schedule
from herbal.services.access_control import get_accessible_subjects


@login_required
def enrollment_create_view(request, pk):

    subjects = get_accessible_subjects(request.user)

    subject = get_object_or_404(subjects, pk=pk)

    # prevent duplicate enrollment
    if hasattr(subject, "enrollment"):
        return redirect("herbal:subjects-detail", pk=subject.pk)

    if request.method == "POST":

        form = EnrollmentForm(request.POST)

        if form.is_valid():

            enrollment = form.save(commit=False)

            enrollment.subject = subject

            enrollment.save()

            # 🔹 generate visit schedule
            generate_visit_schedule(enrollment)

            return redirect(
                "herbal:subjects-detail",
                pk=subject.pk
            )

    else:

        form = EnrollmentForm()

    context = {
        "form": form,
        "subject": subject
    }

    return render(
        request,
        "herbal/enrollments/enrollment_form.html",
        context
    )