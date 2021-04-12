# website-metric-producer

## Introduction

This is a background app that periodically checks the target websites and takes measurements and sends these results to a Kafka topic.

The producer app collects HTTP response time, error code returned, as well as optionally checking the returned page contents for a regexp pattern that is expected to be found on the page.

The list of target URLs, sampling frequency, and regexp pattern are stored and accessible from via a postgres database.

---

## Project Setup

### First Steps

You can begin by either downloading a zip file of the project through github, or using a git command to clone the project by:

```bash
git clone https://github.com/etycomputer/website-metric-producer.git
```

### Virtual Environment Setup

Create a [Python 3.8.1](https://www.python.org/downloads/release/python-381/) based virtual environment (venv) for this project directory.
```bash
virtualenv venv -p python3.8.1
```
After you have your virtual environment directory Setup, you need to activate it.

#### On Linux
```bash
source venv/bin/activate
```
#### On Windows
```bash
venv\Scripts\activate
```
### Dependency installations

To install the necessary packages:

```bash
pip install -r requirements.txt
```

---

##Requirements

This project utilizes the following requirements:

1. Python v3.8.1
1. pytest v6.2.3