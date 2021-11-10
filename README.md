# iCal to JSON

**Version 1.1.0**


This class allows you to take iCal data and turn it into a JSON format. This version supports the following calendar events:

| Calendar Events |
| --------------- |
| VEVENT          |
| VTIMEZONE       |
| STANDARD        |
| DAYLIGHT        |
| VALARM          |
| VTODO           |
| VJOURNAL        |
| VFREEBUSY       |

**Required Imports:**
| Imports   |
| --------- |
| json      |
| requests  |
| os        |
| typing    |
| datetime  |

See example.py, or the documentation for help.

# Documentation

## iCal Settings

When creating the converter object, you must pass an iCalSettings object as well.

> `autoReadableDate` : BOOLEAN : If True, any loaded iCal data will automatically have human readable dates added to it.
>> Defaults to `False`

> `autoRemovePastEvents` : BOOLEAN : If True, any loaded iCal data will automatically have expired events removed from it.
>> Defaults to `False`

## iCal

> `get_json()`
>> Returns the iCal data in its current state.

> `convert_times()`
>> Adds more human readable dates to each event.

> `load_iCal(iCal:str)`
>> Loads new iCal data. This must be raw iCal data, i.e. non-edited iCal data, otherwise an `ICALLoadError` error will be thrown.

> `load_iCal_from_url(url:str)`
>> Loads new iCal data from a URl. This website must return raw iCal data otherwise an `ICALLoadError` error will be thrown.

> `remove_past_events()`
>> Removes all events if their end time is in the past.

> `save_JSON(fileName:str, Optional:filePath:str)`
>> Saves the currently loaded data in a json file.

## Exceptions

> `ICALInvalidSetting`
>> Raised if the defined setting is of the wrong data type.

> `ICALNotLoaded`
>> Raised if a method has been called that requires loaded iCal data, but no iCal data is loaded.

> `ICALLoadError`
>> Raised if the iCal data is of the wrong type, or it is formatted in an unexpected/invalid way.

> `ICALLoadErrorWP`
>> Raised if the iCal data from the specified URL is of the wrong type, or it is formatted in an unexpected/invalid way. This also gives the status codes of the request when raised.

> `ICALInvalidURL`
>> Raised if there was an error connecting to the URL