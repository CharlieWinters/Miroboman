# Miroboman #

Miroboman is an automation web service for facilitating app submisisons to the Miro Marketplace. It works as a middle man between the Marketplace, Jira, Typeform, and Miro itself. 

For the full process flow see [this board](https://miro.com/app/board/uXjVOivZVkk=/). 

# What Miroboman does #

- Automated app checks
    - Valid URLs are provided for provided URLs
    - More to come...
- Creation of Miro board for Design review
- Welcome message with details of review process
- Creation of subtask adding all Marketplace listing assets provided in Typeform response 
- More to come...

Miroboman is a python [fastapi](https://fastapi.tiangolo.com/) application that runs behind a gunicorn webserver.
