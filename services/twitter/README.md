### About 

A simple command line tool that downloads your personal twitter timeline in CSV format with optional keyword filter. More information can be found [here](https://github.com/rasbt/datacollect/tree/master/twitter_timeline).

### Credits

Forked(taken, copied) from [here](https://github.com/rasbt/datacollect/tree/master/twitter_timeline) and originally implemented by [@rasbt](https://github.com/rasbt)

### Dependencies

```
pip install twitter
pip install pandas
pip install pyprind
```

### Usage

For the basic usage create file 'oauth_info.py' with following filled twitter credentials:
```
CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_TOKEN = ''
ACCESS_TOKEN_SECRET = ''
USER_NAME = ''
```

Check file 'run.bat' for running details or execute script using following command line:
```
python twitter_timeline.py -o data/twitter-data.csv
python twitter_user_locations.py -o data/twitter-user-locations-data.csv
```