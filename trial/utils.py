from django.core.mail import EmailMessage


class Utils:

    @staticmethod
    def send_email(data):
        email = EmailMessage(
            # to=kwargs['to'],
            # body=kwargs['body'],
            # subject=kwargs['subject'],
            to=data['to'],
            body=data['body'],
            subject='verify your email',
        )
        email.send()
