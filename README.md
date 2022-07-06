# iCal to JSON

**Version 1.2.0**

## Version 1.2.0 Updates

- Removed iCalSettings. autoReadableDate and autoRemovePastEvents settings are now passed in the iCal constructor.
- Removed iCalSettings errors.
- Added setters and getters for settings
- Added getter for raw iCal data
- Fixed typo in error definitions
- Updated example to reflect affected changes


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

## iCal

When constructing up the iCal object, you can specify some settings. These also come with setter and getter methods.

> `autoReadableDate`: Boolean. If True, any loaded iCal data will automatically have human readable dates added to it.
>> Defaults to `False` 
>> Set value with `set_setting("autoReadableDate", value: bool)`
>> Get value with `get_settings("autoReadableDate")`

> `autoRemovePastEvents`: Boolean. If True, any loaded iCal data will automatically have expired events removed from it.
>> Defaults to `False`
>> Set value with `set_setting("autoRemovePastEvents", value: bool)`
>> Get value with `get_settings("autoRemovePastEvents")`

You can also load your iCal data into the constructor.
> `rawiCal`: String. Raw iCal data, i.e. non-edited iCal data, otherwise an `ICALLoadError` error will be thrown.
>> Defaults to `None` or `""`
>> Set value with `load_iCal(iCal: str)` (see below)
>> Get value with `get_raw_ical()`

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

> `ICALNotLoaded`
>> Raised if a method has been called that requires loaded iCal data, but no iCal data is loaded.

> `ICALLoadError`
>> Raised if the iCal data is of the wrong type, or it is formatted in an unexpected/invalid way.

> `ICALLoadErrorWP`
>> Raised if the iCal data from the specified URL is of the wrong type, or it is formatted in an unexpected/invalid way. This also gives the status codes of the request when raised.

> `ICALInvalidURL`
>> Raised if there was an error connecting to the URL
