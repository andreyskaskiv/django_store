from django.shortcuts import render


def handler_403(request, exception):
    context = {
        'title': 'Forbidden 403',
        'message': str(exception)}
    return render(request,
                  'store/error.html',
                  context=context,
                  status=403)
