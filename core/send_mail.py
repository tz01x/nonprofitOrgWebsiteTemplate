import threading
from django.conf import settings
from django.core.mail import send_mail

from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context

from django.contrib.sites.shortcuts import get_current_site
from django.http import request
# from django.utils.encoding import force_bytes
# from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string

from threading import Thread
from django.core.mail import EmailMessage

class SendMail():
    def _send(self,request,to,subject,templateName,context=None):
        if context :
            message = get_template(templateName).render(context )
        else:
            message=templateName

        mail = EmailMessage(
        subject=subject,
        body=message,
        from_email=settings.EMAIL_HOST_USER,
        to=to,
        reply_to=[settings.EMAIL_HOST_USER],
        )
        mail.content_subtype = "html"
        mail.send()
        
    def sendorBrodcast_WithTemplate(self,request,to,subject,templateName,context):
        '''
        send single email, or brodcast email.

        return an thread that send message 

        '''

        if type(to)==(list or tuple) :
            to=[*to]

        else:

            to=[ to, ]

        
        
        self.current_site = get_current_site(request)
        th=Thread(target=self._send,daemon=True,args=[request,to,subject,templateName,{**context,'site_name':self.current_site}],name='mail_seandingThread')
        th.start()
        # th.join()
        return th 
    def sendorBrodcast_WithoutTemplate(self,request,to,subject,email_body):

        if type(to)==(list or tuple) :
            to=[*to]

        else:

            to=[ to, ]

        
        self.current_site = get_current_site(request)
        th=Thread(target=self._send,daemon=True,args=[request,to,subject,email_body],name='mail_seandingThread_2')
        th.start()
        # th.join()
        return th 




    


