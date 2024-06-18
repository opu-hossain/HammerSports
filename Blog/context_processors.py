from marketing.models import GoogleAnalytics



def analytics(request):
    """
    Context processor for Google Analytics tracking code.

    This function retrieves the first Google Analytics object from the database
    and returns it's code as a dictionary. This dictionary can then be used in
    the templates to add the tracking code if it exists.

    :param request: The HTTP request object.
    :return: A dictionary containing the Google Analytics code if it exists,
             otherwise an empty string.
    """

    # Retrieve the first Google Analytics object from the database
    try:
        ga = GoogleAnalytics.objects.first()
    except GoogleAnalytics.DoesNotExist:
        ga = None

    # If the object exists, return its code, otherwise return an empty string
    code = ga.code if ga else ""

    return {'analytics_code': code}
