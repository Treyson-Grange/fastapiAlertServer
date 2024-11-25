# FastAPI Alert Server

This is a POC (for now) for work. We threw ideas around about this alert system for a while now. Finally coming to fruition.

Meant to be dead simple. If we can sell this to our team, we can start extending to all of USU IT. We think that this will be useful to anyone, and simple enough, that it is well worth it.

The general idea of this is to run it on a box. It more or less acts as a catch all alert system. For example, it will run checks, and when applicable create an alert. Then, we will be able to query the box to get all related alerts. For example, noc will get alerts from here instead of calculating it every x seconds like how I initially developed the alert system.

## Requirements

-   Stick with Python or Typescript (threat).
-   Shouldn't need too many perms, should be able to run with USU firewalls easily.
-   No expiring cert.
-   Scalable, well kept, etc.

## Endpoints

-   `/`: Get a JSON list of all alerts, ordered by criticality then time.
-   `/run-clean`: This will be scheduled, not an endpoint, but it goes through checks timestamp against clearAfter, and removes it if necessary.
-   `/create`: Create an alert.
-   `/delete/{id}`: Delete an alert based on id. (manual acknowledgement)

## Alert Structure

There are two types of alerts: Alerts that will be triggered, added, and displayed till cleared:

-   **Message**: Alert description, purely for display.
-   **Criticality**: There are 3 levels. 0: Critical | 1: Warning | 2: Info.
-   **AutoClear**: Bool to determine whether alert will need manual clear.
-   **Timestamp**: datetime of when the alert was set.
-   **ClearAfter**: Minutes the alert should last.

Additionally, there are manual alerts that will start to appear a specified number of days before their due date. These alerts will increase in criticality as the due date approaches and will automatically clear on the due date.

These alerts can be manually cleared if the event is addressed early.

-   **Expiration Day**: The date when the event occurs.
-   **Days Before**: The number of days before the event when the alert should start appearing.
-   **Message**: The message to display for the event.

Criticality levels will decrease (0 is critical, 2 is informational) as the due date approaches.

## Stack

-   FastAPI: API
-   PeeWee: DB
-   Scheduling: Up in the air
