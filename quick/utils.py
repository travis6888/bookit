import datetime
from googleapiclient.discovery import build
import httplib2
from oauth2client.client import AccessTokenCredentials

__author__ = 'travis6888'




def sign_in_google(request):
    """User logs in through google using python social login. Once the user is logged in, google calendar information is
    pulled from there account. Records of free times are created based on the time in betweeen events"""

    # Pulls information from database about the user
    user_social_auth = request.user.social_auth.get(provider='google-oauth2')
    access_token = user_social_auth.extra_data['access_token']
    calID=user_social_auth.uid
    credentials = AccessTokenCredentials(access_token, 'my-user-agent/1.0')
    http= httplib2.Http()
    http = credentials.authorize(http)

    # Builds service for google calendar
    service = build(serviceName='calendar', version='v3', http=http, developerKey='HFs_k7g6ml38NKohwrzfi_ii')
    current_datetime = datetime.datetime.now().isoformat()[:-3] + 'Z'
    calendar2 = service.events().list(calendarId=calID, timeMin=current_datetime, singleEvents=True,
                                      orderBy='startTime').execute()
    return calendar2

