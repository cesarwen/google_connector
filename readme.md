# Python Libraries for using Google APIs

- Includes ways to connect to both google sheets and google drive

The code was desined for connecting a pandas datafram with google sheets. It is capable of both fetching the google sheets data into a dataframe and adding a dataframe to google sheets

## Capabilities

- Fetch data from google sheets and write it on a pandas dataframe
- Send data from a pandas dataframe into a google sheets
- Download data from a specified google drive folder
- Upload data up to an spcified google drive folder

---
### Quick disclaimer
In order for this piece of code to work you will need to provide your own credentials for the google API (google OAuth).

---
# Usability
This code is usefull the most when paired with a database.
If you can pair it with a database and run queries out of it into a pandas dataframe, it can be sent to the google sheets where dashboards can be created.

This behavior is simillar to tool such as Power BI, periscope and tabular but its implementation.

An example implementation can be found at: [Python Refresh Bot](https://github.com/cesarwen/python_refresh_bot)

It may also be used to feed data from google sheets into the database. Making it able to then save manually inputed data into a database.

---
# Required Libraries

In order for this code to work we must have installed the following libraries:

- pandas
- google api python client
- foofle auth http lib
- google oauth lib

```
pip install pandas
pip install google-api-python-client 
pip install google-auth-httplib2 
pip install google-auth-oauthlib
```

These requirements are the same as for most google apis:

[Gmail API](https://developers.google.com/gmail/api/quickstart/python)

[Google Sheets](https://developers.google.com/people/quickstart/python)

Plus the dataframe library, the core of this code.

# How to Use

### WIP