# datadog

## Description

This script can export monitors from datadog organization.
Also that can import monitors from json files.

## How to use a script

### Install modules

`$ pip3 install datadog-api-client`

### Export monitors

1. You need modify monitor_ids.csv
   1. Write monitor id that you want to export.
2. Run script bellow.
   1. `$ python3 datadog_export_import_monitors_log.py export monitor_ids.csv`
3. Results output to file datadog_monitor.log.

### Import monitors

1. You need monitor json exported file from datadog organization.
2. Run script bellow.
   1. `$ python3 datadog_export_import_monitors_log.py "*.json"`
3. Results output to file datadog_monitor.log.
