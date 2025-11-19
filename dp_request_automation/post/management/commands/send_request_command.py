from typing import Any
from django.core.management.base import BaseCommand, CommandError
import requests
from dp_request_automation.settings import API_URL, API_CREDENTIALS

class Command(BaseCommand):
    help = "Send a POST request to a specified URL with given data."
    headers = {'content-type': 'application/json'}

    def handle(self, *args: Any, **options: Any) -> str | None:
        """The main logic for the management command."""

        # 1. Validate that the API_URL is configured in the environment.
        if not API_URL:
            raise CommandError("The API_URL environment variable is not set. Please configure it in your .env file.")

        try:
            # 2. Prepare the payload and send the POST request.
            self.stdout.write(f"Sending sign-in request...")
            
            # The server expects the credentials to be nested under a "credentials" key.
            payload = {"credentials": API_CREDENTIALS}
            response = requests.post(API_URL, json=payload, headers=self.headers)

            # 3. Check for HTTP errors (e.g., 401 Unauthorized, 500 Server Error).
            # This will raise an exception if the response status code is 4xx or 5xx.
            response.raise_for_status()

            self.stdout.write(
                self.style.SUCCESS(f"Successfully sent POST request to the server.")
            )
        except requests.exceptions.RequestException as e:
            # Handle network-related errors (e.g., connection timeout, DNS failure).
            self.stderr.write(self.style.ERROR(f"Failed to send request: {e}"))
        except Exception as e:
            # Handle any other unexpected errors during the process.
            raise CommandError(f"An unexpected error occurred: {e}")
