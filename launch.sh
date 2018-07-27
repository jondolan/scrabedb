#!/bin/bash

export MONGODB_CONNECTION_STRING=mongodb://localhost:27017/
export SCRAPER_START_DATE="2017-01-01"
python3 app.py
