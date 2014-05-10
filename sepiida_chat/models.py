from django.db import models
from django.template.loader import render_to_string
from django.conf import settings

import os.path
import json
from datetime import datetime
from uuid import uuid4


class Session(models.Model):
    @staticmethod
    def make_key():
        return uuid4().hex

    id = models.CharField(primary_key=True, max_length=255, default=make_key)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)

    ip = models.IPAddressField()
    started = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    replied = models.BooleanField(default=False)
    finished = models.BooleanField(default=False)

    def render(self):
        return render_to_string('sepiida_chat/session.html', {'session': self})

    @classmethod
    def post_message(cls, cid, text, request=None):
        _user = getattr(request, 'user', None)
        user = _user if getattr(_user, 'is_authenticated', lambda:False)() else None

        ip = getattr(request, 'META', {}).get('REMOTE_ADDR', '')

        try:
            session = Session.objects.get(id=cid)
        except Session.DoesNotExist:
            session = Session.objects.create(
                id  = cid,
                user = user,
                ip   = ip,
            )

        return session.message_set.create(
            user = user,
            text = text,
        )


class Message(models.Model):
    session = models.ForeignKey(Session)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)

    timestamp = models.DateTimeField(auto_now_add=True)

    text = models.TextField()

    def render(self):
        return render_to_string('sepiida_chat/message.html', {'message': self})

    @property
    def html(self):
        cached = getattr(self, '_html', None)
        if cached is None:
            cached = self._html = self.render()
        return cached

    def save(self, *args, **kwargs):
        super(Message, self).save(*args, **kwargs)

        chat_store = os.path.join(settings.MEDIA_ROOT, 'sepiida_chat')
        chat_entry = os.path.join(chat_store, '%s.html' % self.session.id)

        try: os.mkdir(settings.MEDIA_ROOT)
        except OSError: pass

        try: os.mkdir(chat_store)
        except OSError: pass

        with open(chat_entry, 'a') as e:
            e.write(self.html.encode('utf-8'))
