import json
import time
from organize_meetings.email_handler import EmailHandler

# Initialize EmailHandler for sending and receiving emails
email_handler = EmailHandler()

class InvitationAgent:
    """
    Agent responsible for sending party invitations and collecting availability responses.
    """
    def run(self, friends_list, invitation_template):
        responses = []
        for friend in friends_list:
            email = friend["email"]
            name = friend["name"]
            message = invitation_template.format(name=name)
            print(f"Sending invitation to {name} at {email}...")
            email_handler.send_email(email, "Party Invitation", message)
            print(f"Waiting for reply from {name}...")
            response = email_handler.wait_for_reply(email)
            responses.append({"email": email, "response": response})
        print("All invitations sent, and responses collected.")
        return responses


class SchedulerAgent:
    """
    Agent responsible for analyzing responses and determining the best schedule.
    """
    def run(self, responses):
        availability = []
        for response in responses:
            email = response["email"]
            reply = response["response"]
            details = self.parse_availability(reply)
            availability.append({"email": email, "details": details})
        best_schedule = self.determine_best_schedule(availability)
        print(f"Proposed schedule determined: {best_schedule}")
        return best_schedule

    def parse_availability(self, reply):
        """
        Parse the response email to extract availability details.
        Expected format: JSON with keys 'times', 'dates', and 'places'.
        """
        try:
            return json.loads(reply)
        except json.JSONDecodeError:
            print(f"Invalid response format: {reply}")
            return {"times": [], "dates": [], "places": []}

    def determine_best_schedule(self, availability):
        """
        Determine the most suitable time, date, and place based on preferences.
        """
        times, dates, places = {}, {}, {}

        for avail in availability:
            details = avail["details"]
            for time in details.get("times", []):
                times[time] = times.get(time, 0) + 1
            for date in details.get("dates", []):
                dates[date] = dates.get(date, 0) + 1
            for place in details.get("places", []):
                places[place] = places.get(place, 0) + 1

        return {
            "time": max(times, key=times.get, default=""),
            "date": max(dates, key=dates.get, default=""),
            "place": max(places, key=places.get, default=""),
        }


class ConfirmationAgent:
    """
    Agent responsible for sending the proposed schedule for confirmation and collecting responses.
    """
    def run(self, friends_list, proposed_schedule):
        confirmations = []
        for friend in friends_list:
            email = friend["email"]
            name = friend["name"]
            message = (
                f"Hi {name},\n\nWe propose the following schedule for the party:\n"
                f"Date: {proposed_schedule['date']}\n"
                f"Time: {proposed_schedule['time']}\n"
                f"Place: {proposed_schedule['place']}\n\n"
                "Please confirm if this works for you by replying to this email."
            )
            print(f"Sending schedule confirmation to {name} at {email}...")
            email_handler.send_email(email, "Party Confirmation", message)
            print(f"Waiting for confirmation from {name}...")
            response = email_handler.wait_for_reply(email)
            confirmations.append({"email": email, "response": response})
        print("All confirmations collected.")
        return confirmations


class NegotiationAgent:
    """
    Agent responsible for renegotiating the schedule if necessary.
    """
    def run(self, confirmations, proposed_schedule):
        disagreements = [
            c for c in confirmations if not self.is_agreeable(c["response"])
        ]
        if disagreements:
            print("Disagreements found. Initiating renegotiation...")
            updated_availability = []
            for disagree in disagreements:
                email = disagree["email"]
                name = email.split("@")[0].capitalize()
                print(f"Renegotiating with {name}...")
                email_handler.send_email(
                    email,
                    "Schedule Renegotiation",
                    "It seems the proposed schedule doesn’t work for you. "
                    "Could you suggest alternative options? Please reply with your preferences."
                )
                reply = email_handler.wait_for_reply(email)
                updated_availability.append(SchedulerAgent().parse_availability(reply))
            print("Updated availability collected. Recalculating schedule...")
            updated_schedule = SchedulerAgent().determine_best_schedule(updated_availability)
            print(f"Updated schedule: {updated_schedule}")
            return updated_schedule
        else:
            print("All invitees agree with the proposed schedule.")
            return proposed_schedule

    def is_agreeable(self, response):
        """
        Determine if the response indicates agreement with the schedule.
        """
        try:
            return json.loads(response).get("agree", False)
        except json.JSONDecodeError:
            print(f"Invalid response format: {response}")
            return False
