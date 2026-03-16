from django.urls import path

from .views.subjects.lists.subject_list_view import subject_list_view
from .views.subjects.creates.subject_create_view import subject_create_view
from .views.subjects.details.subject_detail_view import subject_detail_view
from .views.subjects.updates.subject_update_view import subject_update_view
from .views.visits.visit_dashboard_view import visit_dashboard_view
from .views.visits.visit_mark_missed_view import visit_mark_missed
from .views.screening.screening_create_view import screening_create_view
from .views.screening.screening_update_view import screening_update_view
from .views.enrollments.enrollment_create_view import enrollment_create_view
from .views.enrollments.enrollment_update_view import enrollment_update_view
from .views.crfs.crf1.crf1_create_view import crf1_create_view
from .views.crfs.crf1.crf1_update_view import crf1_update_view
from .views.crfs.crf2.crf2_create_view import crf2_create_view
from .views.crfs.crf2.crf2_update_view import crf2_update_view
from .views.crfs.crf3.crf3_create_view import crf3_create_view
from .views.crfs.crf3.crf3_update_view import crf3_update_view
from .views.crfs.crf4.crf4_create_view import crf4_create_view
from .views.crfs.crf4.crf4_update_view import crf4_update_view
from .views.crfs.crf5.crf5_create_view import crf5_create_view
from .views.crfs.crf5.crf5_update_view import crf5_update_view
from .views.crfs.crf6.crf6_create_view import crf6_create_view
from .views.crfs.crf6.crf6_update_view import crf6_update_view
from .views.crfs.crf7.crf7_create_view import crf7_create_view
from .views.crfs.crf7.crf7_update_view import crf7_update_view

app_name = "herbal"

urlpatterns = [
    # SUBJECTS
    path("subjects/", subject_list_view, name="subjects-list"),
    path("subjects/create/", subject_create_view, name="subject-create"),
    path("subjects/<int:pk>/", subject_detail_view, name="subjects-detail"),
    path("subjects/<int:pk>/edit/", subject_update_view, name="subjects-update"),
    # SCREENING
    path("screening/<int:pk>/", screening_create_view, name="screening-create"),
    path("screening/<int:pk>/update/", screening_update_view, name="screening-update"),
    # ENROLLMENT
    path("enrollment/<int:pk>/", enrollment_create_view, name="enrollment-create"),
    path(
        "enrollment/<int:pk>/update/", enrollment_update_view, name="enrollment-update"
    ),
    # VISITS
    path("visits/dashboard/", visit_dashboard_view, name="visit-dashboard"),
    path("visits/<int:pk>/missed/", visit_mark_missed, name="visit-mark-missed"),
    # CRFS
    # CRF1
    path("crf1/<int:pk>/", crf1_create_view, name="crf1-create"),
    path("crf1/<int:pk>/update/", crf1_update_view, name="crf1-update"),
    # CRF2
    path("crf2/<int:pk>/", crf2_create_view, name="crf2-create"),
    path("crf2/<int:pk>/update/", crf2_update_view, name="crf2-update"),
    # CRF3
    path("crf3/<int:pk>/", crf3_create_view, name="crf3-create"),
    path("crf3/<int:pk>/update/", crf3_update_view, name="crf3-update"),
    # CRF4
    path("crf4/<int:pk>/", crf4_create_view, name="crf4-create"),
    path("crf4/<int:pk>/update/", crf4_update_view, name="crf4-update"),
    # CRF5
    path("crf5/<int:pk>/", crf5_create_view, name="crf5-create"),
    path("crf5/<int:pk>/update/", crf5_update_view, name="crf5-update"),
    # CRF6
    path("crf6/<int:pk>/", crf6_create_view, name="crf6-create"),
    path("crf6/<int:pk>/update/", crf6_update_view, name="crf6-update"),
    # CRF7
    path("crf7/<int:pk>/", crf7_create_view, name="crf7-create"),
    path("crf7/<int:pk>/update/", crf7_update_view, name="crf7-update"),
]
