#!/bin/bash

# Get the current year
current_year=$(date +%Y)

# Loop over the months
for month in $(seq 1 12); do
    # Get the first day of the month
    first_day_of_month=$(date -d "$current_year-${month}-01" +%s)

    # Check if the current time is the first day of the month
    if [ $(date +%s) -eq $first_day_of_month ]; then
        # Run the Python script
        echo "Running Python script for month $month"
        python MIT_jobs_scraper.py $month
    fi
done