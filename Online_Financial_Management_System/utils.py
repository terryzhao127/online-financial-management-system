# Utility functions


def get_alerts(request):
    """
    Collect alerts in session.
    :param request: HttpRequest
    :return: A list of alerts or an empty list
    """
    if 'alerts' in request.session:
        temp = request.session['alerts']
        del request.session['alerts']
        return temp
    else:
        return []
