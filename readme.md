# Python refresh bot implementation

- Includes ways to connect to both google sheets and google drive
- Includes database connection (Snowflake) and a way to fetch data based on a SQL query into a dataframe

The code was desined for refreshing reports on google sheets in a similar way that Power BI, tableau and periscope works.

## What it does:

1. Finds in the google sheets "master" document what are the other google sheets files that we should update.
1. It opens the google sheets file and finds what are the queries and where should their respults be pasted at and where to find then (what is the google drive folder that they are located at).
1. Downloads the queries from the google drive folder, run then and input the query output to the google sheets correct place.
1. Deletes all the downloaded files
1. Repetes from 2 onward for the next file.

---
### Quick disclaimer
- In order for this piece of code to work you will need to provide your own credentials for the google API (google OAuth).
- It is also needed to setup enviromental variables with credentials to the database

---
# Usability
This code was made to mimic the behavior tools such as Power BI, periscope and tabular.

It may also be used to feed data from google sheets into the database. Making it able to then save manually inputed data into a database.

This implementation makes so the user doesn't have to know alot about automation and still makes the automation process of various sheets possible.

---
# Required Libraries

In order for this code to work we must have installed the following libraries:

- pandas
- google api python client
- foofle auth http lib
- google oauth lib

The following libraries depends on the database you are going to use, in my case is snowflake.

- snowflake connector
- sqlalchemy for snowflake

```
pip install pandas
pip install google-api-python-client 
pip install google-auth-httplib2 
pip install google-auth-oauthlib

pip install snowflake-connector-python
pip install snowflake-sqlalchemy
```

These requirements are the same as for most google apis:

[Gmail API](https://developers.google.com/gmail/api/quickstart/python)

[Google Sheets](https://developers.google.com/people/quickstart/python)

Plus the dataframe library, the core of this code.

# How to Use

### WIP
