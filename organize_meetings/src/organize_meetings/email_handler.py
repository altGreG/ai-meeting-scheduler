import os
import base64
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build


class EmailHandler:
    """
    A class to handle sending and receiving emails using the Gmail API.
    """

    def __init__(self):
        self.SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]
        self.creds = self.authenticate()
        self.service = build("gmail", "v1", credentials=self.creds)

    def authenticate(self):
        """
        Authenticate the Gmail API client using OAuth2 credentials.
        Returns:
            Credentials object for Gmail API access.
        """
        creds = None
        # Check if the token.json file exists
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", self.SCOPES)
        # If no valid credentials, perform the OAuth flow
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                from google_auth_oauthlib.flow import InstalledAppFlow
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", self.SCOPES
                )
                creds = flow.run_local_server(port=0)
            # Save the credentials for future use
            with open("token.json", "w") as token:
                token.write(creds.to_json())
        return creds

    def send_email(self, to_email, subject, message_text):
        """
        Send an email to the specified recipient.
        Args:
            to_email (str): Recipient's email address.
            subject (str): Subject of the email.
            message_text (str): Body of the email.
        """
        try:
            message = MIMEText(message_text)
            message["to"] = to_email
            message["subject"] = subject
            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode("utf-8")
            body = {"raw": raw_message}
            self.service.users().messages().send(userId="me", body=body).execute()
            print(f"Email sent to {to_email}.")
        except Exception as error:
            print(f"An error occurred while sending email: {error}")

    def get_latest_email(self, sender_email):
        """
        Fetch the latest email from a specific sender.
        Args:
            sender_email (str): The sender's email address to filter messages.
        Returns:
            str: The plain text body of the latest email, or None if no message is found.
        """
        try:
            # Search for messages from the specified sender
            query = f"from:{sender_email}"
            results = self.service.users().messages().list(userId="me", q=query).execute()
            messages = results.get("messages", [])

            if not messages:
                print(f"No messages found from {sender_email}.")
                return None

            # Get the latest message
            message_id = messages[0]["id"]
            message = self.service.users().messages().get(userId="me", id=message_id).execute()
            payload = message.get("payload", {})
            parts = payload.get("parts", [])

            for part in parts:
                if part.get("mimeType") == "text/plain":
                    body = base64.urlsafe_b64decode(part["body"]["data"]).decode("utf-8")
                    return body

            print("No plain text body found in the email.")
            return None
        except Exception as error:
            print(f"An error occurred while fetching email: {error}")
            return None

    def wait_for_reply(self, sender_email, wait_time=30, max_attempts=10):
        """
        Wait for a reply from a specific sender.
        Args:
            sender_email (str): The sender's email address to monitor.
            wait_time (int): Time in seconds to wait between attempts.
            max_attempts (int): Maximum number of attempts to check for new messages.
        Returns:
            str: The plain text body of the reply email, or None if no reply is received.
        """
        import time

        for attempt in range(max_attempts):
            print(f"Checking for reply from {sender_email} (attempt {attempt + 1}/{max_attempts})...")
            reply = self.get_latest_email(sender_email)
            if reply:
                print(f"Reply received: {reply}")
                return reply
            time.sleep(wait_time)

        print(f"No reply received from {sender_email} after {max_attempts} attempts.")
        return None
