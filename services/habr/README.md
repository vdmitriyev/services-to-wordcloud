### About

Web crawler that extracts specified [habrahabr](http://habrahabr.ru/) user comments and saves them to the CSV file for further processing by the "services-to-wordcloud".

### Usage
Navigate to the source code of the ```habr_user_comments.py``` script and replace the name of the user in the ```dispatcher_dynamic``` python dictionary located at the end of the script. After setting proper name, simply run python script:
```
python habr_user_comments.py
```

### Dependencies

* [beautifulsoup4](https://pypi.python.org/pypi/beautifulsoup4)

Install dependencies with pip
```
pip install -r requirements.txt
```

### Author

* [Viktor Dmitriyev](https://github.com/vdmitriyev/)
