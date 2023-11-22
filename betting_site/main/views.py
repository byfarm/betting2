from django.shortcuts import render
from django.http import HttpResponse
import subprocess
import sys

sys.path.append("~/coding/python/betting")

# Create your views here.


def index(response):
    strg = "Navigate to /nba, /ufc, or /nfl in url"
    return HttpResponse(strg)


def nfl(response):
    # run the scraper
    subprocess.run(["python3", "../runner.py", "NFL"])

    # pull up the excel file
    embed_str = '<iframe src="https://onedrive.live.com/embed?resid=2A3A8CDEE718E8C2%2115197&authkey=!AKm3Goa1XEPFErI&em=2" width="800" height="750" frameborder="0" scrolling="no"></iframe>'
    return HttpResponse(embed_str)


def ufc(response):
    # run the scraper
    subprocess.run(["python3", "../runner.py", "UFC"])

    # pull up the excel file
    embed_str = '<iframe src="https://onedrive.live.com/embed?resid=2A3A8CDEE718E8C2%2115198&authkey=!AOYoEvKo7UbHYYk&em=2" width="700" height="750" frameborder="0" scrolling="no"></iframe>'
    return HttpResponse(embed_str)


def nba(response):
    # run the scraper
    subprocess.run(["python3", "../runner.py", "NBA"])

    # pull up the excel file
    embed_str = '<iframe width="800" height="500" frameborder="0" scrolling="no" src="https://onedrive.live.com/embed?resid=2A3A8CDEE718E8C2%2115203&authkey=%21AEUDpZYPxhkEiZ8&em=2&wdAllowInteractivity=False&wdHideGridlines=True&wdHideHeaders=True&wdInConfigurator=True&wdInConfigurator=True"></iframe>'
    return HttpResponse(embed_str)
