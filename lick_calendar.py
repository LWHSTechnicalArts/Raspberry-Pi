import requests
from icalendar import Calendar

def fetch_ics_data(url):
    try:
        # Fetch the .ics file from the URL
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError if the response was an error

        # Parse the .ics file
        calendar = Calendar.from_ical(response.text)

        # Iterate over calendar events
        for component in calendar.walk():
            if component.name == "VEVENT":
                summary = component.get('summary')
                start = component.get('dtstart')
                end = component.get('dtend')
                description = component.get('description')

                print(f"Summary: {summary}")
                print(f"Start Date: {start.dt if start else 'N/A'}")
                print(f"End Date: {end.dt if end else 'N/A'}")
                print(f"Description: {description}\n")

    except requests.RequestException as e:
        print(f"Error fetching the .ics file: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

# URL of the iCalendar feed
url = 'https://www.lwhs.org/calendar/calendar_349.ics'

# Call the function with the URL
fetch_ics_data(url)
