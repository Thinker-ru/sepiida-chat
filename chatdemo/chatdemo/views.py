from django.shortcuts import render

from uuid import uuid4

def index(request):
    cid = request.session.get('CHAT_ID')
    if not cid:
        cid = request.session['CHAT_ID'] = uuid4().hex
    return render(request, 'index.html', {'CHAT_ID': cid})
