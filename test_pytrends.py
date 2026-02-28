from pytrends.request import TrendReq
pytrends = TrendReq(hl='fr-FR', tz=360)
try:
    print("--- Trending Searches ---")
    df = pytrends.trending_searches(pn='france')
    print(df.head(5))
except Exception as e:
    print(f"Trending Searches failed: {e}")

try:
    print("--- Realtime Trending ---")
    df = pytrends.realtime_trending_searches(pn='FR')
    print(df.head(5))
except Exception as e:
    print(f"Realtime Trending failed: {e}")
