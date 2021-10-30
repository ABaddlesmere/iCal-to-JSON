from iCalToJson import iCal, iCalSettings

#Some raw data
DATA = "BEGIN:VCALENDAR\nX-WR-CALNAME:Example\nX-WR-TIMEZONE:Europe/London\nPRODID:-//Example PRODID v2021//EN\nVERSION:2.0\nBEGIN:VEVENT\nSUMMARY:This is the summary for event1\nLOCATION:This is the location for event1\nDTSTAMP:20210610T110000Z\nDTSTART:20210610T110000\nDTEND:20210610T180000\nCLASS:PUBLIC\nDESCRIPTION:This is the description for event1\nUID:00000000000000000000000000000001\nEND:VEVENT\nBEGIN:VEVENT\nSUMMARY:This is the summary for event2\nLOCATION:This is the location for event2\nDTSTAMP:20210710T110000Z\nDTSTART:20210710T110000\nDTEND:20210710T180000\nCLASS:PUBLIC\nDESCRIPTION:This is the description for event2\nUID:00000000000000000000000000000002\nEND:VEVENT"

#The settings needed for our converter. Leaving these parameters empty will use defaults outlined in the README documentation
settings = iCalSettings(autoReadableDate=True)

#Create the converter using our settings
converter = iCal(settings)

#Load our data into the converter.
#This also formats the data into a dictionary and applies any auto settings, like autoReadableDate
converter.load_iCal(DATA)

#We can get the dictionary by callng get_json()
ourData = converter.get_json()

#Save the data in a json file
converter.saveJson("eventsTest.json")

#Remove past events. This can be called no matter the value of the autoRemovePastEvents setting
converter.remove_past_events()