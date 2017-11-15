from celery import shared_task

from contacts.models import Contact
from phone_numbers.models import PhoneNumber

from .models import Call


@shared_task
def save_call(message):
    record = Call(sid=message.POST['CallSid'],
                  from_number=message.POST['From'],
                  to_number=message.POST['To'])
    record.save()

    if PhoneNumber.objects.filter(e164=message.POST['To']):
        phone_number = PhoneNumber.objects.get(e164=message.POST['To'])
        record.related_phone_number = phone_number
        record.save()
    elif PhoneNumber.objects.filter(e164=message.POST['From']):
        phone_number = PhoneNumber.objects.get(e164=message.POST['From'])
        record.related_phone_number = phone_number
        record.save()

    if Contact.objects.filter(phone_number=message.POST['To']):
        contact = Contact.objects.get(phone_number=message.POST['To'])
        record.related_contact = contact
        record.save()
    elif Contact.objects.filter(phone_number=message.POST['From']):
        contact = Contact.objects.get(phone_number=message.POST['From'])
        record.related_contact = contact
        record.save()


@shared_task
def save_voice_recording(message):
    record = Call.objects.get(sid=message.POST['CallSid'])

    record.recording_url = message.POST['RecordingUrl']
    record.duration = message.POST['RecordingDuration']

    record.save()