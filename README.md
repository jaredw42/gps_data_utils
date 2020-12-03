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
