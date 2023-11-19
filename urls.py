from scrapers.fanduel import scrape_fanduel
from scrapers.pinnacle import scrape_pinnacle
from scrapers.draftkings import scrape_draftkings
from scrapers.betrivers import scrape_betriver
from scrapers.ceasers import scrape_ceasers
from scrapers.mgm import scrape_mgm
from scrapers.pointsbet import scrape_pointsbet

url_db = {
    "UFC": {
        "Ceasers": "https://api.americanwagering.com/regions/us/locations/wa-ms/brands/czr/sb/v3/sports/ufcmma/events/schedule",

        "Draftkings": "https://sportsbook-us-tl.draftkings.com/sites/US-WATL-SB/api/v5/eventgroups/9034?format=json",

        "Betrivers": "https://pa.betrivers.com/api/service/sportsbook/offering/listview/events?t=20239281120&cageCode=268&type=prematch&groupId=1000093883&pageNr=1&pageSize=20&offset=0",

        # "MGM": "https://sports.co.betmgm.com/en/sports/api/widget/widgetdata?layoutSize=Small&page=SportLobby&sportId=45&widgetId=/mobilesports-v1.0/layout/layout_us/modules/ufc/mmalobby&shouldIncludePayload=true",

        "Fanduel": "https://sbapi.nj.sportsbook.fanduel.com/api/content-managed-page?page=SPORT&eventTypeId=26420387&_ak=FhMFpcPWXMeyZxOx&timezone=America%2FNew_York",

        "Pinnacle": "https://guest.api.arcadia.pinnacle.com/0.1/sports/22/markets/straight?primaryOnly=false&withSpecials=false",

        # "Pointsbet": "https://api.va.pointsbet.com/api/v2/competitions/16210/events/featured?includeLive=false&page=1",
    },

    "NFL": {
        "Ceasers": "https://api.americanwagering.com/regions/us/locations/wa-ms/brands/czr/sb/v3/sports/americanfootball/events/schedule",

        "Draftkings": "https://sportsbook-us-co.draftkings.com/sites/US-CO-SB/api/v5/eventgroups/88808?format=json",

        "Betrivers": "https://pa.betrivers.com/api/service/sportsbook/offering/listview/events?t=202310181910&cageCode=268&type=live&type=prematch&groupId=1000093656&pageNr=1&pageSize=10&offset=0",

        # "MGM": None,

        "Fanduel": "https://sbapi.co.sportsbook.fanduel.com/api/content-managed-page?page=CUSTOM&customPageId=nfl&pbHorizontal=false&_ak=FhMFpcPWXMeyZxOx&timezone=America%2FDenver",

        "Pinnacle": "https://guest.api.arcadia.pinnacle.com/0.1/leagues/889/markets/straight",

        "Pointsbet": "https://api.co.pointsbet.com/api/v2/competitions/57/events/featured?includeLive=false&page=1",
    },


    "TEN": {
        "Ceasers": None,

        "Draftkings": None,

        "Betrivers": None,

        # "MGM": None,

        "Fanduel": "https://sbapi.nj.sportsbook.fanduel.com/api/content-managed-page?page=SPORT&eventTypeId=2&_ak=FhMFpcPWXMeyZxOx&timezone=America%2FNew_York",

        "Pinnacle": "https://guest.api.arcadia.pinnacle.com/0.1/sports/33/markets/straight?primaryOnly=false&withSpecials=false",

        "Pointsbet": "https://api.nj.pointsbet.com/api/v2/sports/tennis/events/nextup?limit=50""",
    },
}

scraping_functions: dict = {
        "Ceasers": scrape_ceasers,
        "Draftkings": scrape_draftkings,
        "Betrivers": scrape_betriver,
        "MGM": scrape_mgm,
        "Fanduel": scrape_fanduel,
        "Pinnacle": scrape_pinnacle,
        "Pointsbet": scrape_pointsbet,
}

"""
        "Ceasers": None,
        "Draftkings": None,
        "Betrivers": None,
        "MGM": None,
        "Fanduel": None,
        "Pinnacle": None,
        "Pointsbet": None,
"""
