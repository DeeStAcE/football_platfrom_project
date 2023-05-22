from football.models import League


def list_of_leagues(request):
    return {
        'leagues_list': League.objects.order_by('name')
    }
