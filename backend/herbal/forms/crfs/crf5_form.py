from django import forms
from herbal.models.crfs.crf5.crf5_model import CRF5

class CRF5Form(forms.ModelForm):

    class Meta:

        model = CRF5

        fields = [
            "temperature",
            "blood_pressure",
            "notes",
        ]

        widgets = {

            "temperature": forms.NumberInput(
                attrs={"class": "form-control"}
            ),

            "blood_pressure": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "notes": forms.Textarea(
                attrs={"class": "form-control"}
            ),
        }