import threading
import functools
import logging
from django.core.mail import send_mail
from django.conf import settings

logger = logging.getLogger(__name__)

def async_task(func):
    """
    Decorator that executes a function in a background daemon thread,
    providing .delay() compatibility so call sites work seamlessly without Celery or Redis.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=func, args=args, kwargs=kwargs, daemon=True)
        thread.start()
        return thread
    
    wrapper.delay = wrapper
    return wrapper

@async_task
def send_welcome_email(user_email, full_name):
    """
    Sends a welcome email to newly registered users in a non-blocking background thread.
    """
    try:
        subject = "Welcome to Gridy!"
        message = f"Hello {full_name}, \n\nWelcome to Gridy. We are excited to have you on board!"
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user_email],
            fail_silently=False,
        )
        return f"Sent welcome email to {user_email}"
    except Exception as e:
        logger.error(f"Failed to send welcome email to {user_email}: {e}")