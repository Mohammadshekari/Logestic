from django.conf import settings

def context(request):
    # stuff needed before defining context
    context = {
        "GOOGLE_MAP_API_TOKEN":settings.GOOGLE_MAP_API_TOKEN
        # any other context variables needed
    }
    return context