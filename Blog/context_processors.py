from marketing.models import GoogleAnalytics

def analytics(request):
    ga = GoogleAnalytics.objects.first()
    code = ga.code if ga else ""
    return {'analytics_code': code}