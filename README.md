# Private lesson organizer

## Description

A Django-powered web application that helps teachers organize their private lessons,
students, and homework with an intuitive interface and a fast, reliable backend.

## Features

- **Student Management** - add new students, update their information, or remove them from the teacher’s list when needed.
- **Homework Management** - create, edit, and delete homework assignments once completed by the student.
- **Lesson Management** - schedule upcoming lessons and delete all past ones with a single click.
- **Interactive Calendar** - view all your registered events and lessons in one place.
- **News Feed Integration** - automatically fetches the latest IT headlines via RSS from [The Verge](https://www.theverge.com/).

## Used technologies

| Layer    | Technology                |
|:---------|:--------------------------|
| Backend  | Django 5.2 (Python 3.13)  |
| Database | PostgreSQL                |
| Frontend | HTML, CSS, Bootstrap      |
| Parsing  | Feedparser, BeautifulSoup |

## Installation

### 1. Clone the GitHub repository

```
git clone https://github.com/INBPM0522-TR/web-development-2025-mzsl03.git
```

### 2. Create Virtual environment

- **Conda** 

```
conda create --name <any-name-for-the-env> python=3.12
conda activate <any-name-for-the-env>
```

To get the necessary moduls for the project run:

```
pip install -r requirements.txt
```

- **Pip**

```
python -m venv .venv
Windows (PowerShell/CMD): .venv\Scripts\activate /
Linux and Mac: .venv\Scripts\activate
```

Update pip:

```
python.exe -m pip install --upgrade pip
```

To get the necessary moduls for the project run:

```
pip install -r requirements.txt
```

### 3. .env file

- A valid **.env** file is required for database access. Without it, [Neon.tech](https://neon.com/) will block the connection to the PostgreSQL instance.

- The **.env** file must be created in the root directory of the project, with the following structure:
```
DATABASE_URL=*****
```