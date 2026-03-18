from django.http import JsonResponse
from .models import District, Ward


def get_districts(request):
    region_id = request.GET.get("region_id")
    districts = District.objects.filter(region_id=region_id).values("id", "name")
    return JsonResponse(list(districts), safe=False)


def get_wards(request):
    district_id = request.GET.get("district_id")
    wards = Ward.objects.filter(district_id=district_id).values("id", "name")
    return JsonResponse(list(wards), safe=False)