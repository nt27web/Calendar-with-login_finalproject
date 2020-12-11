from datetime import datetime, timedelta
from cal_setup import get_calendar_service


def create_event(start,end,a):

    service = get_calendar_service()
    event_result = service.events().insert(calendarId='primary',
        body={
            "summary": a,
            "start": {"dateTime": start, "timeZone": 'America/New_York'},
            "end": {"dateTime": end, "timeZone": 'America/New_York'},
        }
    ).execute()

    print("created event")
    print("id: ", event_result['id'])
    print("summary: ", event_result['summary'])
    print("starts at: ", event_result['start']['dateTime'])
    print("ends at: ", event_result['end']['dateTime'])


