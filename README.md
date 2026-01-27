
<h1 align="center">
  PSX-National-News-Sentiment-Analyser
  <br>
</h1>

<h4 align="center">Generate News Sentiment Using Machine Learning models</h4>


<p align="center">
  <a href="#key-features">Key Features</a> •
  <a href="#how-to-use">How To Use</a> •
  <a href="#download">Download</a> •
  <a href="#license">License</a>
</p>


## Key Features

* Sentiment Analyzer - create sentiment for national news positive, negative and neutral.
* Tag news headline
* Symbol Occurrence - check if symbol is mentional in news if it is then generate an alert.


## How To Use

To clone and run this application, you'll need [Git](https://git-scm.com) and [Python](https://www.python.org/downloads/) (which comes with [pip](https://pip.pypa.io/en/stable/installation/)) installed on your computer. From your command line:

```bash
# Clone this repository
$ git clone https://github.com/psx-bot/psx-news-sentiment.git


# Install dependencies
$ pip3 install fastapi
$ pip install "uvicorn[standard]"

# install uvicorn
$ sudo apt install uvicorn

# install nltk and scikit learn
$ python3 -m pip install nltk
$ python3 -m pip install scikit-learn

# Run the app
$ sh ./start_dev

# Add newly install lib in requirements file
$ pip3 install -U fastapi

# if requirements file is not found then create from pip3
$ pip3 freeze > requirements.txt

# Run unit tests
$ python3 -m unittests -v

# Removing dependencies list 
$ sed -i 's/search_string/replace_string/' filename

```

> **Note**
> If you're using Linux Bash for Windows, [see this guide](https://www.howtogeek.com/261575/how-to-run-graphical-linux-desktop-applications-from-windows-10s-bash-shell/) or use `python` from the command prompt.


## Download

You can [download](hhttps://github.com/orgs/psx-bot/packages) the latest docker image version.

## Related


## License

MIT
