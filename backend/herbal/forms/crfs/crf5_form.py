from django import forms
from herbal.models.crfs.crf5.crf5_model import CRF5


class CRF5Form(forms.ModelForm):

    class Meta:

        model = CRF5

        fields = [
            "event_date",
            "event_description",
            "severity",
            "action_taken",
            "outcome",
        ]

        widgets = {
            "event_date": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "event_description": forms.Textarea(attrs={"class": "form-control"}),
            "severity": forms.Select(attrs={"class": "form-control"}),
            "action_taken": forms.Textarea(attrs={"class": "form-control"}),
            "outcome": forms.Textarea(attrs={"class": "form-control"}),
        }
