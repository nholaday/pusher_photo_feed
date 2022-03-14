from django.shortcuts import render, HttpResponse
from django.conf import settings
from django.http import JsonResponse
from pusher import Pusher
from feed.models import Feed
from feed.forms import DocumentForm

# instantiate pusher
pusher = Pusher(
    app_id=settings.PUSHER_APP_ID, 
    key=settings.PUSHER_APP_KEY,
    secret=settings.PUSHER_APP_SECRET,
    cluster=settings.PUSHER_APP_CLUSTER,
)


def index(request):
    """ get all current photos ordered by the latest """
    all_documents = Feed.objects.all().order_by('-id')
    return render(request, 'index.html', {'all_documents':all_documents})


def pusher_authentication(request):
    """ function that authenticates the private channel """
    channel = request.GET.get('channel_name', None)
    socket_id = request.GET.get('socket_id', None)
    auth = pusher.authenticate(
        channel = channel,
        socket_id = socket_id,
    )

    return JsonResponse(json.dumps(auth), safe=False)


def push_feed(request):
    if request.method == "POST":
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            f = form.save()
            # trigger a pusher request after saving the new feed element
            pusher.trigger(u'a_channel', u'an_event', {u'description': f.description, u'document': f.document.url})
            return HttpResponse('ok')
        else:
            return HttpRespone('form not valid')
    else:
        return HttpResponse('error, please try again')



