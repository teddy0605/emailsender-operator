import logging
from mailersend import emails
import json
import logging

logger = logging.getLogger(__name__)

class EmailProvider:
    def send_email(self, sender_email, recipient_email, subject, body):
        raise NotImplementedError("This method should be overridden by subclasses.")


class MailerSendProvider(EmailProvider):
    def __init__(self, api_token):
        self.mailer = emails.NewEmail(api_token)
        
    def send_email(self, sender_email, recipient_email, subject, body):
        mail_body = {}
        self.mailer.set_mail_from({"name": "Operator", "email": sender_email}, mail_body)
        self.mailer.set_mail_to([{"name": "", "email": recipient_email}], mail_body)
        self.mailer.set_subject(subject, mail_body)
        self.mailer.set_plaintext_content(body, mail_body)
        
        response = self.mailer.send(mail_body)

        try:
            response_data = json.loads(response)
            logger.info(f"Email sent with response: {json.dumps(response_data, indent=2)}")
            return {'status': 'sent', 'response': response_data}
        
        except (json.JSONDecodeError, TypeError):
            return {'status': 'error', 'message': 'Invalid response format'}


class UnknownEmailProvider(EmailProvider):
    def __init__(self, api_token=None):
        pass

    def send_email(self, sender_email, recipient_email, subject, body):
        logger.error("Simulated error: Service unavailable.")
        return {"status": "error", "provider": "UnknownEmailProvider", "message": "Service unavailable"}

email_providers = {
    "mailersend": MailerSendProvider,
    "unknownprovider": UnknownEmailProvider
}
