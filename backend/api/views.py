from datetime import datetime, timedelta

from django.http import JsonResponse
from django.core.serializers import serialize

from .models import RawMini, RawTsi


def parse_dttm(dttm):
    return datetime.strptime(dttm, '%Y-%m-%dT%H:%M:%S')


def parse_request(request):
    try:
        start = parse_dttm(request.GET.get('start'))
    except (TypeError, ValueError):
        start = datetime(2021, 10, 28)
    try:
        end = parse_dttm(request.GET.get('end'))
    except (TypeError, ValueError):
        end = datetime.utcnow() + timedelta(hours=2)
    return start, end


def query_data(request, model):
    start, end = parse_request(request)
    queryset = model.objects.filter(dttm__gte=start, dttm__lte=end)
    data = [x for x in queryset.values('dttm', 'conc')]
    return data


def raw_mini(request):
    return JsonResponse(query_data(request, RawMini), safe=False)


def raw_tsi(request):
    return JsonResponse(query_data(request, RawTsi), safe=False)
