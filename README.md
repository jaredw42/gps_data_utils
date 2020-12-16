# gps_data_utils
utility scripts for gnss data


## timecalc
converts UTC epoch time or UTC datetime to GPS weeks and seconds.

leap seconds are just hardcoded to 18 for now. 
```
timecalc 2020-12-02 11:59:59
UTC DATETIME: 2020-12-02 11:59:59
GPS WEEK: 2134, TOW: 302417.0
```

## trim_data
trims a large gnss data file to a smaller TOW range 
doesnt handle the TOW rollover nicely right now. 

```
➜  gps_data_utils git:(main) ✗ ./trim_data.py -h
trim_data started
usage: trim_data.py [-h] -filepath FILEPATH [-tow TOW TOW]

arguments:
  -h, --help            show this help message and exit
  -filepath FILEPATH, -f FILEPATH
                        path to .sbp or .sbp.json file
  -tow TOW TOW, -t TOW TOW
                        start time and end time in GPSTOW
  ```
