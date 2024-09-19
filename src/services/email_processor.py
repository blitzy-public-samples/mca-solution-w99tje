import imaplib
from email import message_from_bytes
from email.header import decode_header
from typing import List, Dict, Any
from src.core.config import settings
from src.services.document_classifier import DocumentClassifier
from src.api.models.application import Application
from src.api.models.document import Document
from sqlalchemy.orm import Session
from src.core.database import SessionLocal
from src.utils.logger import logger

class EmailProcessor:
    """Class for processing incoming emails and extracting relevant information"""

    def __init__(self):
        """Initialize the EmailProcessor"""
        # Initialize IMAP client using settings
        self.imap_client = imaplib.IMAP4_SSL(settings.EMAIL_SERVER, settings.EMAIL_PORT)
        # Login to email server
        self.imap_client.login(settings.EMAIL_USERNAME, settings.EMAIL_PASSWORD)
        # Initialize DocumentClassifier
        self.document_classifier = DocumentClassifier()

    def process_emails(self) -> List[Dict[str, Any]]:
        """Process new emails in the inbox"""
        processed_emails = []

        try:
            # Select the inbox
            self.imap_client.select('INBOX')

            # Search for unread emails
            _, message_numbers = self.imap_client.search(None, 'UNSEEN')

            for num in message_numbers[0].split():
                # Fetch the email content
                _, msg_data = self.imap_client.fetch(num, '(RFC822)')
                email_body = msg_data[0][1]
                email_message = message_from_bytes(email_body)

                # Parse the email
                email_data = self.parse_email(email_message)

                # Extract relevant information
                application_data = {
                    'applicant_name': email_data['sender'],
                    'application_date': email_data['date'],
                    'status': 'Received'
                }

                # Classify and save attachments
                attachments = []
                for attachment in email_data['attachments']:
                    attachment_info = self.save_attachment(attachment)
                    attachments.append(attachment_info)

                # Create Application and Document records
                with SessionLocal() as db:
                    application = Application(**application_data)
                    db.add(application)
                    db.flush()

                    for attachment in attachments:
                        document = Document(
                            application_id=application.id,
                            file_path=attachment['file_path'],
                            document_type=attachment['document_type']
                        )
                        db.add(document)

                    db.commit()

                # Mark email as read
                self.imap_client.store(num, '+FLAGS', '\\Seen')

                processed_emails.append({
                    'application_id': application.id,
                    'email_subject': email_data['subject'],
                    'attachments': attachments
                })

            # Close the IMAP connection
            self.imap_client.close()
            self.imap_client.logout()

        except Exception as e:
            logger.error(f"Error processing emails: {str(e)}")

        # Return processed email data
        return processed_emails

    def parse_email(self, email_message: message_from_bytes) -> Dict[str, Any]:
        """Parse an email message and extract relevant information"""
        # Extract subject
        subject, encoding = decode_header(email_message['Subject'])[0]
        if isinstance(subject, bytes):
            subject = subject.decode(encoding or 'utf-8')

        # Extract sender
        sender, encoding = decode_header(email_message['From'])[0]
        if isinstance(sender, bytes):
            sender = sender.decode(encoding or 'utf-8')

        # Extract body
        if email_message.is_multipart():
            body = ''
            for part in email_message.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode()
                    break
        else:
            body = email_message.get_payload(decode=True).decode()

        # Extract attachments
        attachments = []
        for part in email_message.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get('Content-Disposition') is None:
                continue
            attachments.append(part)

        # Return extracted data
        return {
            'subject': subject,
            'sender': sender,
            'body': body,
            'date': email_message['Date'],
            'attachments': attachments
        }

    def save_attachment(self, attachment: Any) -> Dict[str, Any]:
        """Save an email attachment and classify it"""
        # Get attachment filename
        filename = attachment.get_filename()

        # Save attachment to temporary file
        file_path = f"/tmp/{filename}"
        with open(file_path, 'wb') as f:
            f.write(attachment.get_payload(decode=True))

        # Classify document using DocumentClassifier
        document_type = self.document_classifier.classify(file_path)

        # Return attachment information
        return {
            'file_path': file_path,
            'document_type': document_type
        }

# Human tasks:
# 1. Review and adjust email parsing logic if needed
# 2. Implement error handling and retries for IMAP operations
# 3. Add additional security measures for handling attachments
# 4. Implement a mechanism to handle duplicate emails or applications
# 5. Add logging for important events and errors