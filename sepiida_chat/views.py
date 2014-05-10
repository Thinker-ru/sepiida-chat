from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

import os.path
import json
from datetime import datetime
from uuid import uuid4

@csrf_exempt
def send(request):
    # check request
    if request.method != 'POST':
        return HttpResponse('boo')

    text = request.POST.get('text', '').strip()
    if not text:
        raise ValueError('No text.')

    page_title = request.POST.get('title', '').strip()
    page_path = request.POST.get('path', '').strip()

    cid = request.session.get('CHAT_ID')
    print cid
    if not cid:
        raise ValueError('User with no CHAT_ID!')

    # setup store
    chat_store = os.path.join(settings.MEDIA_ROOT, 'sepiida_chat')
    chat_entry = os.path.join(chat_store, '%s.html' % cid)
    chat_meta = os.path.join(chat_store, '%s.json' % cid)

    try: os.mkdir(settings.MEDIA_ROOT)
    except OSError: pass

    try: os.mkdir(chat_store)
    except OSError: pass

    # format entry
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = "<div><span>%s</span> %s</div>" % (ts, text.replace('<', '&lt;'))
    meta = json.dumps({
        'text': text,
        'timestamp': ts,
        'path': page_path,
        'title': page_title,
        'ip': request.META.get('REMOTE_ADDR')
    })

    # update chat log
    with open(chat_entry, 'a') as e:
        e.write(entry.encode('utf-8'))

    with open(chat_meta, 'a') as m:
        m.write(meta)

    return HttpResponse(entry)

def js(request):
    cid = request.session.get('CHAT_ID')
    if not cid:
        cid = request.session['CHAT_ID'] = uuid4().hex
    return render(request, 'sepiida_chat/widget.js', {'CHAT_ID': cid})

