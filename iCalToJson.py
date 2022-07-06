import json
import requests
import datetime
from typing import Union
import os
import urllib3

DAY_SUFFIX = {
    "1":"st",
    "2":"nd",
    "3":"rd"
}
MONTH_CONVERTER = {
    "01":"Janurary",
    "02":"Februaru",
    "03":"March",
    "04":"April",
    "05":"May",
    "06":"June",
    "07":"July",
    "08":"August",
    "09":"September",
    "10":"October",
    "11":"November",
    "12":"December"
}
TIME_CONVERTER ={
    "00":"0",
    "01":"1",
    "02":"2",
    "03":"3",
    "04":"4",
    "05":"5",
    "06":"6",
    "07":"7",
    "08":"8",
    "09":"9",
    "10":"10",
    "11":"11",
    "12":"12",
    "13":"1",
    "14":"2",
    "15":"3",
    "16":"4",
    "17":"5",
    "18":"6",
    "19":"7",
    "20":"8",
    "21":"9",
    "22":"10",
    "23":"11",
}

class Base_ICAL_Error(Exception):
    def __init__(self,main,extra):
        self.main=main
        self.extra=extra
        super().__init__(self.main)

    def __str__(self):
        if self.extra == "":
            return f"{self.main} -> No Other Information Given"
        else:
            return f"{self.main} -> {self.extra}"

class ICalLoading(Base_ICAL_Error):
    def __init__(self, extra):
        super().__init__("Error loading iCal data", extra)

class ICalEditor(Base_ICAL_Error):
    def __init__(self, extra):
        super().__init__("Error trying to edit iCal data", extra)

class ICALNotLoaded(ICalEditor):
    def __init__(self, evidence:Union[str, None]):
        extra = "There is currently no iCal data loaded. Please load some data and try again"
        super().__init__(extra)

class ICALLoadError(ICalLoading):
    def __init__(self, evidence:Union[str, None]):
        extra = "The iCal you tried to load is not correct type or is in an invalid format. iCal data must be of type STRING and begin with 'BEGIN:VCALENDAR'"
        if evidence is not None:
            extra += f"[{type(evidence)}]"
            if type(evidence) == str:
                extra += f" [{evidence[:15]}]"
        super().__init__(extra)

class ICALLoadErrorWP(ICalLoading):
    def __init__(self, evidence:Union[requests.Response, None]):
        extra = "The iCal you tried to load is not correct type or is in an invalid format. iCal data must be of type STRING and begin with 'BEGIN:VCALENDAR'"
        if evidence is not None:
            extra += f"[{type(evidence)}]"
            if type(evidence) == requests.Response:
                extra += f" [{evidence.text[:15]}] [STATUS CODE: {evidence.status_code} {evidence.reason}]"
        super().__init__(extra)

class ICALInvalidURL(ICalLoading):
    def __init__(self, evidence:Union[str, None]):
        extra = "The URL you passed did not exist or there was an issue connecting to it"
        if evidence is not None:
            extra += f"[{evidence}]"
            if type(evidence) == str:
                extra += f" [{evidence[:15]}]"
        super().__init__(extra)



class iCal:
    def __init__(self, autoReadableDate: bool=False, autoRemovePastEvents: bool=False, rawiCal:str=""):
        self.__autoReadableDate = autoReadableDate
        self.__autoRemovePastEvents = autoRemovePastEvents
        self.__rawICAL = ""
        self.__ICAL = {}
        if rawiCal != "":
            self.load_iCal(rawiCal)
        else:
            self.__rawICAL = ""

    def __auto_settings(self):
        '''
        Assumes ICAL has already been converted to dict
        '''
        if self.__autoReadableDate:
            self.convert_times()
        if self.__autoRemovePastEvents:
            self.remove_past_events()

    def __validate_iCal(self, iCal:str) -> bool:
        '''
        Returns true is the iCal passed is of type string and begins with VCALENDAR
        '''
        if isinstance(iCal, str) and iCal[:15] == "BEGIN:VCALENDAR":
            return True
        else:
            return False

    def __has_ical_loaded(self) -> bool:
        '''
        Returns True is there is currently an iCAL loaded
        '''
        return self.__rawICAL != ""

    def __object_string_to_2dlist(self, rawICAL: str) -> list:
        '''
        Returns a list of events
        '''
        temp1 = rawICAL.split("\nBEGIN:")
        temp2 = []
        for item in temp1:
            temp2.append(item.split("\n"))
        return temp2

    def __object_list_to_dict(self, ICAL2d: list) -> dict:
        '''
        Returns a dictionary of events/objects
        '''
        objectDict = {}
        validObjects = {
            "VCALENDAR": 0,
            "BEGIN:VCALENDAR": 0,
            "VEVENT": 0,
            "VTIMEZONE": 0,
            "STANDARD": 0,
            "DAYLIGHT": 0,
            "VALARM": 0,
            "VTODO": 0,
            "VJOURNAL": 0,
            "VFREEBUSY": 0
            }
        for entry in ICAL2d:
            if entry[0] in validObjects:
                if entry[0] == "BEGIN:VCALENDAR":
                    entry[0] = "VCALENDAR"
                validObjects[entry[0]] += 1
                entryKey = f"{entry[0]}{validObjects[entry[0]]}"
                objectDict[entryKey] = {}
                for value in entry:
                    if ":" in value and "END" not in value:
                        temps = value.split(":", 1)
                        objectDict[entryKey][temps[0]] = temps[1]
                    elif ":" in value and "DTEND" in value:
                        temps = value.split(":", 1)
                        objectDict[entryKey][temps[0]] = temps[1]
                    else:
                        continue

        for key, _ in validObjects.items():
            validObjects[key] = 0

        return objectDict

    def __requestFromWebpage(self, url: str) -> Union[str, None]:
        '''
        Sends a request to the URL and returns the text response
        '''
        print("[iCalToJson] Waiting for a response from the webpage...")
        try:
            rawdata = requests.get(url)
        except urllib3.exceptions.NewConnectionError:
            raise ICALInvalidURL(evidence=url)
        
        if self.__validate_iCal(rawdata.text) and rawdata.status_code == 200:
            return rawdata.text
        else:
            raise ICALLoadErrorWP(rawdata)

    def __format_object_times(self):
        '''
        Adds readable dates and times to the events
        '''
        if not self.__has_ical_loaded():
            raise ICALNotLoaded()
        for key, event in self.__ICAL.items():
            if "DTSTAMP" not in event:
                continue
            event['ReadableDTSTART'] = ""
            event['ReadableDTEND'] = ""
            for subkey, subvalue in event.items():
                if subkey == "DTSTART":
                    event['ReadableDTSTART'] = self.__DTtime_to_readable_time(subvalue)
                elif subkey == "DTEND":
                    event['ReadableDTEND'] = self.__DTtime_to_readable_time(subvalue)

    def __DTtime_to_readable_time(self, DTtime: str) -> str:
        '''
        Converts and returns the string of numbers (20211007T230000) from DTSTART/DTEND
        to times, days, months and years
        '''
        dateAndTime = DTtime.split("T")
        date = dateAndTime[0]
        time = dateAndTime[1]
        
        day = date[6:]
        day = day[1] if day[0] == "0" else day    #Removes the 0 if the day is single digits
        daySuffix = DAY_SUFFIX[day] if day in "1 2 3" else "th"    #Determines the suffix for the day
        readableDate = f"{day}{daySuffix} {MONTH_CONVERTER[date[4:6]]}, {date[0:4]}"

        readableTime = f"{time[0:2]}:{time[2:4]} (24Hr) / {TIME_CONVERTER[time[0:2]]}:{time[2:4]}{'AM' if int(time[0:2]) <= 11 else 'PM'} (12Hr)"

        readableDT = f"{readableDate} at {readableTime}"

        return readableDT

    def set_setting(self, setting: str, value: bool) -> None:
        '''
        Sets the setting to the new value
        '''
        if setting == "autoReadableDate":
            self.__autoReadableDate = value
        if setting == "autoRemovePastEvents":
            self.__autoRemovePastEvents = value

    def get_setting(self, setting: str) -> bool:
        '''
        Returns the value for the specified setting
        '''
        if setting == "autoReadableDate":
            return self.__autoReadableDate
        if setting == "autoRemovePastEvents":
            return self.__autoRemovePastEvents

    def get_raw_ical(self) -> str:
        '''
        Returns the raw iCal data provided by the user
        '''
        return self.__rawICAL

    def get_json(self) -> dict:
        '''
        Returns the iCal events as a json format (dict)
        '''
        return self.__ICAL

    def convert_times(self):
        '''
        Public method for adding more human readable times and dates
        '''
        self.__format_object_times()

    def load_iCal(self, iCal:str):
        '''
        Public method for loading new an iCal string
        '''
        if self.__validate_iCal(iCal):
            self.__rawICAL = iCal
            ICAL2d = self.__object_string_to_2dlist(self.__rawICAL)
            self.__ICAL = self.__object_list_to_dict(ICAL2d)
            self.__auto_settings()
        else:
            raise ICALLoadError(evidence=iCal)

    def load_iCal_from_url(self, url:str):
        '''
        Public method for loading iCal from a URL
        '''
        data = self.__requestFromWebpage(url)
        self.load_iCal(data)


    def remove_past_events(self):
        '''
        Public method for removing events whose DTEND is in the past
        '''
        if not self.__has_ical_loaded():
            raise ICALNotLoaded()
        currentDateTime = datetime.datetime.now().__str__().replace("-","").replace(" ","").replace(":","")[:14]
        poppableKeys = []
        for key, event in self.__ICAL.items():
            for subkey, subvalue in event.items():
                if subkey == "DTEND":
                    if int(self.__ICAL[key][subkey].replace("T","")) <= int(currentDateTime):
                        poppableKeys.append(key)

        for key in poppableKeys:
            self.__ICAL.pop(key)

    def save_JSON(self, fileName:str, filePath:str=""):
        '''
        Public method for saving iCal as JSON
        '''
        fileName += ".json" if ".json" not in fileName else ""
        
        if filePath != "":
            os.chdir(filePath)
        with open(fileName,"w") as jsonFile:
            json.dump(self.__ICAL, jsonFile, indent=4)

