# PyJiraTT
Simple Python script, which provides command line interface to fetch time spent per day per issue in Jira.
Name stands for "Python Jira Time Tracking".

## Install
Make sure you have Python 3 installed and also for convenience you can create sym link:
```bash
ln -s ~/src/pyjiratt/pyjiratt.py ~/bin/jiratt
```


## Usage
```bash
jiratt -h
usage: jiratt [-h] [--since SINCE] [--until UNTIL] [-v] [-vv]
              [--jira-url JIRA_URL] [--jira-user JIRA_USER]
              [--jira-pass JIRA_PASS] [--jira-assignee JIRA_ASSIGNEE]
              [--jira-storypoints-field JIRA_STORYPOINTS_FIELD]
              [--max-results MAX_RESULTS]

optional arguments:
  -h, --help            show this help message and exit
  --since SINCE         date in YYYY-MM-DD format or JIRA date function
  --until UNTIL         date in YYYY-MM-DD format or JIRA date function
  -v                    increase output verbosity
  -vv                   increase output verbosity more
  --jira-url JIRA_URL   JIRA url, e.g. https://www.jira.com
  --jira-user JIRA_USER
                        JIRA user name
  --jira-pass JIRA_PASS
                        JIRA user password
  --jira-assignee JIRA_ASSIGNEE
                        JIRA assignee
  --jira-storypoints-field JIRA_STORYPOINTS_FIELD
                        JIRA story points
  --max-results MAX_RESULTS
                        maximum of issues to fetch
```
JIRA parameters can also be configured via environment variables, e.g. in ~/.bashrc:
```bash
export JIRA_URL=https://www.jira.com/
export JIRA_USER=user
export JIRA_PASS=pass
export JIRA_ASSIGNEE=name
export JIRA_STORYPOINTS_FIELD=customfield_10002
```
## Example output

### Output format by default
```bash
2018-01-15 Mon: 8h
2018-01-16 Tue: 8h
2018-01-17 Wed: 8h
2018-01-18 Thu: 8h
2018-01-19 Fri: 8h
```
### More verbose output with -v flag:
```bash
2018-01-15 Mon: 8h
    DS-5269: 8h
2018-01-16 Tue: 8h
    DS-5269: 8h
2018-01-17 Wed: 8h
    DS-5261: 8h
2018-01-18 Thu: 8h
    DS-5266: 8h
2018-01-19 Fri: 8h
    DS-5268: 6h
    DS-5265: 2h
```
### Even more verbose output with -vv flag:
```bash
2018-01-29 Mon: 8h
  DS-5302:
    Title: Write script to dump data into Clickhouse
    Link: https://www.jira.com/browse/DS-5302
    Status: Done
    Reporter: Alexander Bocharov
    Worklog timespent: 8h
    Original estimate: 24h
    Total timespent: 24h
    Estimate accuracy: 100.00%
2018-01-30 Tue: 8h
  DS-5361:
    Title: Develop cool feature X1
    Link: https://www.jira.com/browse/DS-5361
    Status: Done
    Reporter: Alexander Bocharov
    Worklog timespent: 4h
    Original estimate: 4h
    Total timespent: 4h
    Estimate accuracy: 100.00%
  DS-5302:
    Title: Write script to dump data into Clickhouse
    Link: https://www.jira.com/browse/DS-5302
    Status: Done
    Reporter: Alexander Bocharov
    Worklog timespent: 4h
    Original estimate: 24h
    Total timespent: 24h
    Estimate accuracy: 100.00%
2018-01-31 Wed: 8h
  DS-5303:
    Title: Improve API performance
    Link: https://www.jira.com/browse/DS-5303
    Status: Done
    Reporter: Alexander Bocharov
    Worklog timespent: 4h
    Original estimate: 8h
    Total timespent: 8h
    Estimate accuracy: 100.00%
  DS-5302:
    Title: Write script to dump data into Clickhouse
    Link: https://www.jira.com/browse/DS-5302
    Status: Done
    Reporter: Alexander Bocharov
    Worklog timespent: 4h
    Original estimate: 24h
    Total timespent: 24h
    Estimate accuracy: 100.00%
2018-02-01 Thu: 8h
  DS-5303:
    Title: Improve API performance
    Link: https://www.jira.com/browse/DS-5303
    Status: Done
    Reporter: Alexander Bocharov
    Worklog timespent: 4h
    Original estimate: 8h
    Total timespent: 8h
    Estimate accuracy: 100.00%
  DS-5301:
    Title: Fix critical bug in parsing component
    Link: https://www.jira.com/browse/DS-5301
    Status: Done
    Reporter: Alexander Bocharov
    Worklog timespent: 4h
    Original estimate: 16h
    Total timespent: 14h
    Estimate accuracy: 87.50%
2018-02-02 Fri: 8h
  DS-5301:
    Title: Fix critical bug in parsing component
    Link: https://www.jira.com/browse/DS-5301
    Status: Done
    Reporter: Alexander Bocharov
    Worklog timespent: 8h
    Original estimate: 16h
    Total timespent: 14h
    Estimate accuracy: 87.50%
```