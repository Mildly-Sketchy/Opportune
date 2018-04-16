# Opportune

**Author**: Kat Cosgrove, Gene Pieterson, Patricia Raftery, Austin Matteson
**Version**: 1.0.0

## Overview

Opportune is a web application that uses a web scraper and keywords from the user to find jobs in their area related to their chosen search terms. To use, the user must register or log in, choose their location and job keywords, and Opportune will email to them a list of 20 job postings within their specifications. At any time the user can go back and search again, with different keywords/city, or if they use the same they will not get the same job postings again. The user has the ability to unsubscribe to Opportune at any time.

## How It Works

This application returns 20 job postings to the user on submit of their location and keyword preferences. It does this by using Beautiful Soup to scrape Indeed.com. The results are stored in a csv file and emailed to the user.

## Getting Started

To replicate this app, you would fork and clone our GitHub https://github.com/Mildly-Sketchy/Opportune. Then you would need to start a virtual environment, install the packages to get the dependencies used in this app, and have 3 empty databases set up.

## Architecture

Three SQL databases are used for persistence to store job postings and user data. Pyramid is used for the framework, and the web scraper used is Beautiful Soup. Other technologies used are Python3, Travis CI, Jupyter notebook, pandas, HTML, CSS, and JavaScript. Heroku is used for deployment.

## Change Log

#### Prework

04/10/2018 1400 - Discussed project ideas

04/11/2018 1400 - Selected project idea

04/12/2018 1400 - Did wireframes and planning

04/13/2018 1400 - Created repository

04/13/2018 1400 - Created front-end mock-ups

04/15/2018 1400 - Created Pyramid framework

#### Day 1

04/16/2018 1000 - Deployed scaffolded site with Heroku

04/16/2018 1100 - Travis CI utilized

#### Day 2

## Credits and Collaborations
