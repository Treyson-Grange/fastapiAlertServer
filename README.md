# FastAPI Alert Server

This is a POC (for now) for work. We threw ideas around about this alert system for a while now. Finally coming to fruition.

Meant to be dead simple. If we can sell this to our team, we can start extending to all of USU IT. We think that this will be useful to anyone, and simple enough, that it is well worth it.

The general idea of this is to run it on a box. It more or less acts as a catch all alert system. For example, it will run checks, and when applicable create an alert. Then, we will be able to query the box to get all related alerts. For example, noc will get alerts from here instead of calculating it every x seconds like how I initially developed the alert system.

## Requirements

-   Stick with Python or Typescript (threat).
-   Shouldn't need too many perms, should be able to run with USU firewalls easily.
-   No expiring cert.
-   Scalable, well kept, etc.

## Structure

The main functionality of the project has been split into several files.

-   `main.py`: Entry point for the `FastAPI` server. Sets up middleware to allow for CORS.
-   `routes.py`: Set up and expose all API requests. Allows for the retrieval of all alerts, the creation of alerts, and the deletion of alerts.
-   `schemas.py`: Defines `pydantic` models for use within `FastAPI`. Defines our two alerts, (manual and auto) and defines which attribute
    s are sent via API.
-   `models.py`: Defines `peewee` database models. Defines our two stored alerts (manual and auto).
-   `utils.py`: Contains all miscellaneous functions for use within our app. (Verification, calculations, etc)
-   `database.py`: Simply connect to our `peewee` database
-   `createdb.py`: Standalone script to create a database file in your directory.
-   `backup_script.py`: Script designed to be run as a CRON job to create and store backups of the database.

## Endpoints

-   `/alerts`: GET a JSON list of all alerts, both manual and auto, sort them by criticality and timestamp
-   `/run-clean`: GET request to run a job that will be cronified later
-   `/create`: POST request to create an auto alert.
-   `/create-manual`: POST request to create a manual alert.
-   `/delete/{id}`: POST request to delete an alert based on id. (acknowledgement)
-   `/delete-manual/{id}`: POST request to Delete a manual alert based on id. (acknowledgement)

Testing only endpoints:

-   `/all`: GET a JSON list of all alerts, no group required.
-   `/groups`: GET a JSON list of all groups in our database. No group endpoints will be created, groups is a internal utility only.

## Alert Structure

There are two types of alerts:

Auto Alerts: Will be triggered, added, and displayed till cleared:

-   `message`: Alert description, purely for display.
-   `criticality`: There are 3 levels. 0: Critical | 1: Warning | 2: Info.
-   `autoClear`: Bool to determine whether alert will need manual clear.
-   `timestamp`: datetime of when the alert was set.
-   `clearAfter`: Minutes the alert should last.
-   `group`: Group that the alert belongs to/will be sent to.

Manual Alerts: Start to appear a specified number of days before their due date. These alerts will increase in criticality as the due date approaches and will automatically clear on the due date.

These alerts can be manually cleared if the event is addressed early.

-   `dueDate`: The date when the event occurs.
-   `daysNotice`: The number of days before the event when the alert should start appearing.
-   `message`: The message to display for the event.
-   `group`: Group that the alert belongs to/will be sent to.

Criticality levels decrease (0 is critical, 2 is informational) as the due date approaches.

## Stack

-   `FastAPI`: API Web framework
-   `PeeWee`: DataBase ORM
-   `Scheduling`: Up in the air

## Food for thought / Mind Dump

-   For auto alerts, we should change it so on creation, we create the date object ourselves, so we know its in the correct format.
