from herbal.models import VisitSchedule


def update_visit_status(visit):

    # Do not modify if visit is terminated / NA
    if visit.status == "na":
        return

    required_forms = ["crf2", "crf3", "crf4", "crf7"]

    if visit.visit_day == "D0":
        required_forms.append("crf1")

    completed = True

    for form in required_forms:
        if not hasattr(visit, form):
            completed = False
            break

    if completed:
        visit.status = "completed"

        if not visit.actual_visit_date:
            visit.actual_visit_date = visit.scheduled_date

        visit.save()