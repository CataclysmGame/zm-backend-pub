<div align="center">
    <a href="https://github.com/CataclysmGame/cyberjump-backend">
        <img src="./assets/logo.png" width="80" height="60">
    </a>

<h3 align="center">Cataclysm: Zero Mission Game Server</h3>
</div>

<details>
    <summary>Table of Contents</summary>
    <ol>
        <li>
            <a href="#about-the-project">About the Project</a>
        </li>
        <li>
            <a href="#how-it-works">How it works</a>
        </li>
        <li>
            <a href="#getting-started-locally">Getting Started Locally</a>
            <ul>
                <li><a href="#prerequisites">Prerequisites</a></li>
                <li><a href="#running">Running</a></li>
            </ul>
        </li>
        <li>
            <a href="#getting-started-with-docker">Getting Started with Docker</a>
            <ul>
                <li><a href="#docker-prerequisites">Prerequisites</a></li>
                <li><a href="#docker-running">Running</a></li>
            </ul>
        </li>
        <li>
            <a href="#for-developers">For Developers</a>
            <ul>
                <li>
                </li>
            </ul>
        </li>
    </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

This is the server used to save highscores for [Cataclysm: Zero Mission](https://www.cataclysm-game.com/zero-mission)


### Built with
* [Python](https://www.python.org/)
* [Poetry](https://python-poetry.org/docs/)
* [FastAPI](https://fastapi.tiangolo.com/)
* [SQLModel](https://sqlmodel.tiangolo.com/)

## How it works
The server receives high score submissions on a public API interface.
Before sending any score record, the game must request a ticket on another API.
The ticket should then be included into score submissions. After a ticked is used,
it will be invalidated therefore a new ticked should be requested before submitting a new record.

Every request is validated by an anti-cheat component.

A set of basic admin APIs is also included to allow for trivial management operations, like banning users.

<!-- GETTING STARTED LOCALLY -->
## Getting Started Locally
This section contains instructions on how to set up this
project locally.

### Prerequisites

* [Python ^3.9.0](https://www.python.org/)
* [Poetry](https://python-poetry.org/docs/)

Installing Poetry ([Official documentation](https://python-poetry.org/docs/#installation)):

```
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
```

### Running

`cd` into the project directory and run:
```
poetry update
```
This command will create a new Poetry virtual environment if none already exists and install all
dependencies.
Now you can start both the API service and the Faust worker.

```
# Start the API service
python -m app
```

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- GETTING STARTED WITH DOCKER -->
## Getting Started with Docker
This section contains instructions on how to set up this
project using [Docker](https://www.docker.com/).

### Prerequisites <a id='docker-prerequisites'></a>

* [Docker](https://www.docker.com/)
* [Docker Compose](https://docs.docker.com/compose/)

[Install Docker](https://docs.docker.com/get-docker/) then
[Install Docker Compose](https://docs.docker.com/compose/install/)

### Running <a id='docker-running'></a>

`cd` into the project directory and run:
```
docker-compose up
```
This will start the server and the database instance.

<p align="right">(<a href="#top">back to top</a>)</p>
