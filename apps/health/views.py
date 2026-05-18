from django.db import connection
from django.http import HttpResponse


def healthz(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
    except Exception:
        return HttpResponse(status=503)

    return HttpResponse(status=200)
