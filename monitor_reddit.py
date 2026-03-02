import requests
import json
import os
from datetime import datetime

def monitor_threads(username="Dalcim972", threads=[]):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json',
        'Accept-Language': 'fr-FR,fr;q=0.9,en;q=0.8',
    }
    feedback = {
        "direct_replies": [],
        "positive": [],
        "negative_bugs": [],
        "suggestions": [],
        "last_scan": datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
    }
    
    for url in threads:
        print(f"--- Monitoring Thread: {url} ---")
        # Use old.reddit.com which is more permissive
        json_url = url.replace("reddit.com", "old.reddit.com").rstrip('/') + ".json"
        try:
            response = requests.get(json_url, headers=headers, timeout=15)
            if response.status_code == 200:
                data = response.json()
                comments = data[1]['data']['children']
                
                def find_and_harvest_replies(comment_list):
                    for comment in comment_list:
                        if comment['kind'] == 't1':
                            c_data = comment['data']
                            
                            if c_data.get('author') == username:
                                my_timestamp = c_data.get('created_utc')
                                print(f"   [Found {username} at {datetime.fromtimestamp(my_timestamp)}]")
                                
                                replies = c_data.get('replies')
                                if replies and replies != '' and 'data' in replies:
                                    for reply in replies['data']['children']:
                                        if reply['kind'] == 't1':
                                            r_data = reply['data']
                                            r_body = r_data.get('body', '')
                                            r_ts = r_data.get('created_utc')
                                            
                                            if r_ts > my_timestamp:
                                                entry = {
                                                    "author": r_data.get('author'),
                                                    "text": r_body,
                                                    "timestamp": datetime.fromtimestamp(r_ts).strftime('%Y-%m-%d %H:%M:%S'),
                                                    "url": f"https://reddit.com{r_data.get('permalink')}"
                                                }
                                                feedback["direct_replies"].append(entry)
                                                
                                                low_body = r_body.lower()
                                                if any(w in low_body for w in ["merci", "super", "top", "génial", "bravo"]):
                                                    feedback["positive"].append(entry)
                                                elif any(w in low_body for w in ["bug", "marche pas", "erreur", "problème"]):
                                                    feedback["negative_bugs"].append(entry)
                                                elif any(w in low_body for w in ["faudrait", "idée", "ajouter", "possible"]):
                                                    feedback["suggestions"].append(entry)
                            
                            replies = c_data.get('replies')
                            if replies and replies != '' and 'data' in replies:
                                find_and_harvest_replies(replies['data']['children'])
                                
                find_and_harvest_replies(comments)
                print(f"   ✅ OK ({len(comments)} top-level comments)")
                
            else:
                print(f"⚠️  {url}: HTTP {response.status_code}")
        except Exception as e:
            print(f"❌ Error processing {url}: {e}")

    output_path = "feedback_report.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(feedback, f, ensure_ascii=False, indent=4)
    
    return feedback

if __name__ == "__main__":
    test_threads = [
        "https://reddit.com/r/france/comments/1rf5lrl/au_chômage_et_la_caf_me_réclame_une_dette/",
        "https://reddit.com/r/france/comments/1rfq8hs/aide_pour_caf/"
    ]
    res = monitor_threads(threads=test_threads)
    print(f"\nScan terminé. Réponses directes : {len(res['direct_replies'])}")
