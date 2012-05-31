
import traceback

from django.conf.urls.defaults import patterns, include
from django.http import HttpResponseNotFound, HttpResponseServerError


def handle_404(request):
    return HttpResponseNotFound("- 404 -")

def handle_500(request):
    message = "Error caught in handler500 for tests\n" + traceback.format_exc()
    print message
    return HttpResponseServerError(message)


handler404 = __name__ + '.handle_404'
handler500 = __name__ + '.handle_500'

urlpatterns = patterns('',
    (r'^', include(__name__.rsplit('.', 3)[0] + '.urls'))
)
