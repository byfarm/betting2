# betting2
This sports betting scraper scrapes betting odds for the UFC, NBA, and the NFL. It collects the data, does some data analysis on it to find profitable bets, then writes the results to an excel file. A simple django website then displays the excel file so that every time the page is refreshed, the scrapers are run again.

The scrapers use python's asycio module to quickly run the scrapes so when the website's page is refreshed, it takes less than 8 seconds to show the new results; an essential feature with quick-moving sportsbetting odds.

Notable Python modules used in this project is httpx to make the async requests, and pandas to print and format the excel file. 

Profitable betts are calculated by taking a shart sportsbook (in this case Pinnacle Sportsbook) and finding the no-vig odds from that sportsbook. The odds from other sportsbooks are then compared against these odds to determine if thier bets are statistically profitable. Other usefull data is displayed along with the results including the kelly number (what percent of your bankroll you should place into one bet), the expected value of the bet, the average no-vig odds from all the sportsbooks, and the spread on the event given by Pinnacle Sportsbook.
