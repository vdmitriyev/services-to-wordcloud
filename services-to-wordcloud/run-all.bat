@echo off
REM @author Viktor Dmitriyev
echo "NOTE: Running this script can take a lot of your processing time."
start python github-to-wordcloud.py
start python orcid-to-wordcloud.py
start python rss-to-wordcloud.py
start python tumblr-to-wordcloud.py
start python twitter-to-wordcloud.py
start python habr-to-wordcloud.py
