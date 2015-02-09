### About
Tiny python utility that converts data crawled from different services into cloud of words.

### Supported Services so Far
* [Twitter](https://twitter.com/)

### Credits
* Heavily inspired by the article [Turn Your Twitter Timeline into a Word Cloud Using Python](http://sebastianraschka.com/Articles/2014_twitter_wordcloud.html#A.-Downloading-Your-Twitter-Timeline-Tweets) written by [@rasbt](https://github.com/rasbt)
* Fonts are taken from the various of places and initially distributed by the authors under one of the open licenses. A huge collection of fonts can be found in the [googlefontdirectory github repository](https://github.com/w0ng/googlefontdirectory).

### Examples Generated

![](./examples/twitter-wordcloud-arvo-regular-square_mask-black.png)
![](./examples/twitter-wordcloud-monaco-twitter_mask-white.png)


### Installation
Use 'pip' to install dependencies
```
pip install matplotlib
pip install twitter 
pip install pyprind
pip install numpy
pip install matplotlib
pip install pandas
pip install scipy
```

Or use 'conda' from Anaconda to install dependencies (*better solutions in case you are new to python or Windows user*):
```
conda install matplotlib
conda install twitter 
conda install pyprind
conda install numpy
conda install matplotlib
conda install pandas
conda install scipy
```
If you are not able to find package 'by default' with 'conda', please use 'binstar' to find proper binary of the package. For example for 'twitter' it looks like this:
```
binstar search -t conda twitter
```

Installing [wordcloud](https://github.com/amueller/word_cloud) package can be very tricky
```
pip install git+git://github.com/amueller/word_cloud.git
conda install pil
```

### Author
* [Viktor Dmitriyev](https://github.com/vdmitriyev)

###  License

Check this file with [license](LICENSE)
