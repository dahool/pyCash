"""BSD License
Copyright (c) 2008, Adolfo Custidiano Secchi 
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

 * Redistributions of source code must retain the above copyright notice,
   this list of conditions and the following disclaimer.
 * Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation and/or 
   other materials provided with the distribution.
 * Neither the name of the <ORGANIZATION> nor the names of its contributors may be used
   to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR
IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS
BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA,
OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""
try:
  from xml.etree import ElementTree
except ImportError:
  from elementtree import ElementTree
import gdata.calendar.service
import gdata.service
import atom.service
import gdata.calendar
import atom
import getopt
import sys
import string
import time
import datetime
import calendar
import iso8601


"""GoogleApi is a python way to interact with the Google Calendar. 

  GoogleApi: Provides methods to login in Google Calendar, 
             get all the calendar feeds, insert new events,
             add participant to an event and define when to
              send notifications to them and for the last
             get all the participant associated to an event
             and for each participant get his attendee status  
             
  Version:  0.1 Adolfo Custidiano Secchi 
                First release
               
            0.2 Sergio Gabriel Teves
                License change.
                Added possibility to update and delete events.
                All google events are now wrapped in a custom Event class
            
                  NOTICE: methods insertSingleEvent and getEventByTitle are
                      not compatible with previous version.
                      
            0.2.1 Sergio Gabriel Teves
                Fix time conversion issue
            0.2.2 Adolfo Custidiano 
                Feature to delete attendees attached to an event.
                Fix some bugs on previous features.
            0.3 Sergio Gabriel Teves
                Add getEventById, addGuest, removeGuest, and some error controls
            0.3.1 Sergio Gabriel Teves
                Fix url conversion issue on findbyId
"""

"""Event class, for google events isolation.
   
   Considerations:
       eventElement is used to talk with google. do not manually modify it.
"""
class Event:
    title = ""
    description = ""
    location = ""
    dateFrom = None
    dateTo = None
    eventElement = None
    id = None
    
    def __init__(self, **kwargs):
        if 'title' in kwargs:
            self.title = kwargs['title']
        if 'description' in kwargs:
            self.description = kwargs['description']
        if 'location' in kwargs:
            self.location = kwargs['location']
        if 'dateFrom' in kwargs:
            self.dateFrom = kwargs['dateFrom']
        if 'dateTo' in kwargs:
            self.dateTo = kwargs['dateTo']
        if 'eventElement' in kwargs:
            self.eventElement = kwargs['eventElement']
            self.id = self.eventElement.id.text.split("/")[-1]
        if 'id' in kwargs:
            self.id = kwargs['id']
    
    def setEventId(self,  evt):
        self.id = evt.id.text.split("/")[-1]
        
class GoogleApi:

    ca_client = None
    account_email = None
    eventUrl = '/calendar/feeds/default/private/full'
    
    def __init__(self, username, password):
        """Initialize ca_client and accout_email,
            ca_client provides all the google services available
            by Google Api.

            Args:
                username: a str that contain the full @gmail username,
                password: a str that contain the google's account password. 
        """ 
        
        self.account_email = username
        self.ca_client = self.getCalendarService(username, password)
    
    def getCalendarService(self, username, password):
        """ getCalendarService: login to the google calendar service

            Args:
                username: a str that contain the full @gmail username,
                password: a str that contain the google's account password. 
            
            Returns:
                ca_client: gdata.calendar.service.CalendarService instance             
        """
        cal_client = gdata.calendar.service.CalendarService()
        cal_client.email = username
        cal_client.password = password
        cal_client.source = 'Google Calendar Python Service'
        cal_client.ProgrammaticLogin()
        return cal_client
    
    def getCalendarFeeds(self):
        """ getCalendarFeeds: get all the feeds associated to the 
                            calendar.

            Requires:
                    Must instanciate a GoogleApi class to 
                    get login to GoogleCalendar.
            
            Returns:
                feeds: a list of all the events registered in 
                the calendar.             
        """
        feed = cal_client.GetAllCalendarsFeed()
        return feed
    
    def myEventToGEvent(self, myEvent):
        """ convert from local event object to google atom event
        """
        event = gdata.calendar.CalendarEventEntry()
        event.title = atom.Title(text=myEvent.title)
        event.content = atom.Content(text=myEvent.description)
        event.where.append(gdata.calendar.Where(value_string=myEvent.location))
        
        if isinstance(myEvent.dateFrom,datetime.date):
            tupleStart = myEvent.dateFrom.timetuple();
        else:
            tupleStart = myEvent.dateFrom
            
        if isinstance(myEvent.dateTo,datetime.date):
            tupleEnd = myEvent.dateTo.timetuple();
        else:
            tupleEnd = myEvent.dateTo            
            
        # GOOGLE REQUIRES THE TIME TO BE UTC
        from_datetime = time.gmtime(time.mktime(tupleStart))
        to_datetime = time.gmtime(time.mktime(tupleEnd))        
        
        start_time = time.strftime('%Y-%m-%dT%H:%M:%S.000Z', from_datetime)
        end_time = time.strftime('%Y-%m-%dT%H:%M:%S.000Z', to_datetime)

        event.when.append(gdata.calendar.When(start_time=start_time, end_time=end_time))        
        
        return event
        
    def GEventToMyEvent(self, event):
        """ convert google atom event to a local event object
        """
        for a_where in event.where:
            a_location = a_where.value_string
        for a_when in event.when:
            startTime = a_when.start_time
            endTime = a_when.end_time
        
        # GOOGLE RETURN THE TIME IN THE GCALENDAR TIMEZONE IN ISO8601 
        startTime = iso8601.parse_date(startTime)
        endTime = iso8601.parse_date(endTime)
        
        myEvent = Event(title=event.title.text, description=event.content.text, 
                        location=a_location, dateFrom=startTime, dateTo=endTime,
                        eventElement=event)
        
        return myEvent
        
    def insertSingleEvent(self, myEvent):
        """ insertSingleEvent: Insert a new event into the calendar.

            Considerations:
                    title must be unique between all 
                    the events, this is CRITICAL to the other functions to work.
            
            Returns:
                    the Event
        """
        event = self.myEventToGEvent(myEvent)
        try:
            myEvent.eventElement = self.ca_client.InsertEvent(event, self.eventUrl) 
            myEvent.setEventId(myEvent.eventElement)
            return myEvent
        except:
            return False

    def getEventById(self,  eventId):
        try:
            event  = self.ca_client.GetCalendarEventEntry(str(self.eventUrl + "/%s" % eventId))
            return self.GEventToMyEvent(event)
        except:
            return False
            
    def getEventByTitle(self, title):
        """ getEventByTitle: query an event matching the passed Title.
                        
            Returns:
                    the last matching Event.
        """
        event = None
        query = gdata.calendar.service.CalendarEventQuery('default', 'private', 'full', title)
        feed = self.ca_client.CalendarQuery(query)

        if len(feed.entry)>0:
            for i, an_event in enumerate(feed.entry):
                event = an_event
            myEvent = self.GEventToMyEvent(event)
        else:
            myEvent = False
              
        return myEvent
    
    def updateEvent(self, myEvent):
        event = self.myEventToGEvent(myEvent)
        self.ca_client.UpdateEvent(myEvent.eventElement.GetEditLink().href, event)
#        try:
#            self.ca_client.UpdateEvent(myEvent.eventElement.GetEditLink().href, event)
#            return True
#        except:
#            return False
        
    def deleteEvent(self, myEvent):
        try:
            self.ca_client.DeleteEvent(myEvent.eventElement.GetEditLink().href)
            return True
        except:
            return False
    
    def addGuest(self, myEvent, name, email, notify = True):
        """ addGuest: Add new guest to the passed event.
                        
            Args:
                myEvent (REQUIRED): the event to update
                contactName (REQUIRED): Guest name
                contactMail (REQUIRED): Guest e-mail
                notify: send notification

            Returns:
                    true if success
        """
        event = myEvent.eventElement
        event.who.append(gdata.calendar.Who(name=name, email=email))
        notification = gdata.calendar.SendEventNotifications(value=notify)
        event.send_event_notifications = notification
        self.ca_client.UpdateEvent(event.GetEditLink().href, event)
        try:

            return True
        except:
            return False
    
    def removeGuest(self, myEvent, contactMail):
        """ removeGuest: Remove guest from the passed Event
                        
            Args:
                myEvent (REQUIRED): the event to update
                contactMail (REQUIRED): Guest e-mail
                
            Returns:
                    true if success
        """
        
        event = myEvent.eventElement
        participant_element = None
        for p, participant in enumerate(event.who):
            if participant.email == contactMail:
                participant_element = participant
                break
        event.who.remove(participant_element)
        try:
            self.ca_client.UpdateEvent(event.GetEditLink().href, event)
            return True
        except:
            return False

    def getGuestStatus(self, eventId, contactMail):
        """ getGuestStatus: get a participant status that match with the 
                                    given email address in an specific EventId.
                        
            Args:
                EventId
                contactMail
                
            Returns:
                AttendeeStatus instance. See Google Api. / False if failed
        """
        
        attendee_status = False
        
        myEvent = self.getEventById(eventId)

        if myEvent != False:
            event = myEvent.eventElement
            for p, participant in enumerate(event.who):
                if contactMaill == participant.email:
                    attendee_status = participant.attendee_status
                    break
        
        return attendee_status

    #@deprecated
    def invitePeople(self, titleId, name, email, notifyByMail):
        """ invitePeople: Invite a contact to the event matching Title
        
            This method is deprecated. Use addGuest instead.
                        
            Args:
                titleId(REQUIRED): str that concatenate match with this ID-TITLE, 
                                defined when you insert the event.
                contactName(REQUIRED): str that contains the Event Participant Name. 
                contactMail(REQUIRED): str that contains the Event Participant Email.
                notify(REQUIRED): str (true or false) that define if will be send a 
                                    notification to the participant email.
                
            Requires:
                    Must instanciate a GoogleApi class to 
                    get login to GoogleCalendar.
                    
                    id argument must be unique between all 
                    the events that that will insert, this
                    is CRITICAL to the others functions.
                    
                    titleId MUST match with this pattern ID-TITLE, 
                    defined when you insert the event.
            
            Returns:
                    event: Google Calendar Event Class. See Google Api.
        """
        event = self.getEventByTitle(titleId)
        event_src = event.eventElement
        event_src.who.append(gdata.calendar.Who(name=name, email=email))
        notification = gdata.calendar.SendEventNotifications(value=notifyByMail)
        event_src.send_event_notifications = notification
        self.ca_client.UpdateEvent(event_src.GetEditLink().href, event_src)
        return event
    
    #@deprecated
    def removePeople(self, titleId, email):
        """ removePeople: Remove People from the event.
        
            This method is deprecated. Use removeGuest instead.
                        
            Args:
                titleId(REQUIRED): str that concatenate match with this ID-TITLE, 
                                defined when you insert the event.
                name(REQUIRED): str that contains the Event Participant Name. 
                email(REQUIRED): str that contains the Event Participant Email.
                
            Requires:
                    Must instanciate a GoogleApi class to 
                    get login to GoogleCalendar.
                    
                    id argument must be unique between all 
                    the events that that will insert, this
                    is CRITICAL to the others functions.
                    
                    titleId MUST match with this pattern ID-TITLE, 
                    defined when you insert the event.
            
            Returns:
                    event: Google Calendar Event Class. See Google Api.
        """
        
        event = self.getEventByTitle(titleId)
        event_src = event.eventElement 
        participant_element = None
        for p, participant in enumerate(event_src.who):
            if participant.email == email:
                participant_element = participant
                break
        event_src.who.remove(participant_element)
        self.ca_client.UpdateEvent(event_src.GetEditLink().href, event_src)
        return event
    
    def getAttendeeStatusByEmail(self, titleId, email):
        """ getAttendeeStatusByEmail: get a participant status that match with the 
                                    given email address in an specific Event wich Title 
                                    is like this Pattern ID-TITLE.
                        
            Args:
                titleId(REQUIRED): str that concatenate match with this ID-TITLE, 
                                defined when you insert the event. This will be 
                                used to find the event.
                email(REQUIRED): str that contains the Event Participant Email. 
                
            Requires:
                    Must instanciate a GoogleApi class to 
                    get login to GoogleCalendar.
                    
                    id argument must be unique between all 
                    the events that that will insert, this
                    is CRITICAL to the others functions.
                    
                    titleId MUST match with this pattern ID-TITLE, 
                    defined when you insert the event.
            
            Returns:
                    attendee_status: is an AttendeeStatus instance. See Google Api. 
        """
        
        event = None
        attendee_status = None
        query = gdata.calendar.service.CalendarEventQuery('default', 'private', 'full', titleId)
        feed = self.ca_client.CalendarQuery(query)
        for i, an_event in enumerate(feed.entry):
            event = an_event
            for p, participant in enumerate(event.who):
                if self.account_email != participant.email:
                    if participant.email == email:
                        attendee_status = participant.attendee_status
                        break
        return attendee_status
    
    def getAttendees(self, titleId):
        """ getAttendees: get all the Participants in a specific Event wich Title 
                        match with this Pattern ID-TITLE.
                        
            Args:
                titleId(REQUIRED): str that concatenate match with this ID-TITLE, 
                                defined when you insert the event. This will be 
                                used to find the event. 
                
            Requires:
                    Must instanciate a GoogleApi class to 
                    get login to GoogleCalendar.
                    
                    id argument must be unique between all 
                    the events that that will insert, this
                    is CRITICAL to the others functions.
                    
                    titleId MUST match with this pattern ID-TITLE, 
                    defined when you insert the event.
            
            Returns:
                    who: List of who associated to the Event. See Google Api.
        """

        who = None
        query = gdata.calendar.service.CalendarEventQuery('default', 'private', 'full', titleId)
        feed = self.ca_client.CalendarQuery(query)
        for i, an_event in enumerate(feed.entry):
            who = an_event.who            
        return who

def googleApiTest(googleUser,  googlePass, guestMail = "test@test.com"):
    
    now = datetime.datetime.now()
    difference1 = datetime.timedelta(days=1)
    difference2 = datetime.timedelta(hours=2)
    fDate = now + difference1
    tDate = fDate + difference2
    
    # INSERT EVENT
    event = Event(title="Event Test",  dateFrom=fDate,  dateTo=tDate)
    calendar = GoogleApi(googleUser,  googlePass)
    newEvent = calendar.insertSingleEvent(event)
    
    if newEvent == False:
        raise Exception("INSERT FAILED")
    
    print "INSERT PASSED"
    
    # GET EVENT BY ID
    event = calendar.getEventById(newEvent.id)

    if event != False and event.id == newEvent.id:
        print "FIND BY ID PASSED"
    else:
        raise Exception("FIND BY ID FAILED")

    # UPDATE
    event.title = "New Event Title"
    r = calendar.updateEvent(event)
    
    if r == False:
        raise Exception("UPDATE FAILED")
        
    print "UPDATE PASSED"

    # UPDATE EDIT LINK
    event = calendar.getEventById(newEvent.id)

    #REMOVE EVENT
    r = calendar.deleteEvent(event)

    if r == False:
        raise Exception("REMOVE EVENT FAILED")

    print "REMOVE EVENT PASSED"

    print "ALL TEST PASSED"

'''
   # ADD GUEST
    r = calendar.addGuest(event,"test",guestMail)

    if r == False:
        raise Exception("ADD GUEST FAILED")

    print "ADD GUEST PASSED"
    
    # GET GUEST STATUS
    status = calendar.getGuestStatus(event.id,  guestMail)
    
    if status == False:
        raise Exception("GET GUEST STATUS FAILED")

    print "GET GUEST STATUS PASSED"
    
    # REMOVE GUEST
    
    # UPDATE EDIT LINK
    event = calendar.getEventById(newEvent.id)
    
    r = calendar.removeGuest(event,  guestMail)
    
    if r == False:
        raise Exception("REMOVE GUEST FAILED")

    print "REMOVE GUEST PASSED"

    # UPDATE EDIT LINK
    event = calendar.getEventById(newEvent.id)
'''