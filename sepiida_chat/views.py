from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import admin

from .models import Session

@csrf_exempt
def send(request):
    # check request
    if request.method != 'POST':
        return HttpResponse('boo')

    text = request.POST.get('text', '').strip()
    if not text:
        raise ValueError('No text.')

    cid = get_cid(request)
    if not cid:
        raise ValueError('User with no CHAT_ID!')

    message = Session.post_message(cid, text, request)
    return HttpResponse(message.html)


def js(request):
    cid = get_cid(request)
    return render(request, 'sepiida_chat/widget.js', {'CHAT_ID': cid})


def get_cid(request):
    if request.user.is_staff and request.REQUEST.get('cid'):
        cid = request.REQUEST['cid']
    else:
        cid = request.session.get('CHAT_ID')
        if not cid:
            cid = request.session['CHAT_ID'] = Session.make_key()

    return cid
