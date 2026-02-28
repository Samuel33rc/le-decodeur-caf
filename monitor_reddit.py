import requests
import json
import os
from datetime import datetime

def monitor_threads(username="Dalcim972", threads=[]):
    headers = {'User-agent': 'Le-Decodeur-CAF-Monitor-v1.1'}
    feedback = {
        "direct_replies": [],
        "positive": [],
        "negative_bugs": [],
        "suggestions": []
    }
    
    for url in threads:
        print(f"--- Monitoring Thread: {url} ---")
        json_url = url.rstrip('/') + ".json"
        try:
            response = requests.get(json_url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                # data[1] is the comment tree
                comments = data[1]['data']['children']
                
                def find_and_harvest_replies(comment_list):
                    for comment in comment_list:
                        if comment['kind'] == 't1': # It's a comment
                            c_data = comment['data']
                            
                            # If author is our target user, we harvest their replies
                            if c_data.get('author') == username:
                                my_timestamp = c_data.get('created_utc')
                                print(f"   [Found {username} at {datetime.fromtimestamp(my_timestamp)}]")
                                
                                # Check if there are replies
                                replies = c_data.get('replies')
                                if replies and replies != '' and 'data' in replies:
                                    for reply in replies['data']['children']:
                                        if reply['kind'] == 't1':
                                            r_data = reply['data']
                                            r_body = r_data.get('body', '')
                                            r_ts = r_data.get('created_utc')
                                            
                                            # We only take replies posted AFTER our comment
                                            if r_ts > my_timestamp:
                                                entry = {
                                                    "author": r_data.get('author'),
                                                    "text": r_body,
                                                    "timestamp": datetime.fromtimestamp(r_ts).strftime('%Y-%m-%d %H:%M:%S'),
                                                    "url": f"https://reddit.com{r_data.get('permalink')}"
                                                }
                                                feedback["direct_replies"].append(entry)
                                                
                                                # Classification simple
                                                low_body = r_body.lower()
                                                if any(w in low_body for w in ["merci", "super", "top", "génial", "bravo"]):
                                                    feedback["positive"].append(entry)
                                                elif any(w in low_body for w in ["bug", "marche pas", "erreur", "problème"]):
                                                    feedback["negative_bugs"].append(entry)
                                                elif any(w in low_body for w in ["faudrait", "idée", "ajouter", "possible"]):
                                                    feedback["suggestions"].append(entry)
                            
                            # Recursive call for nested comments
                            replies = c_data.get('replies')
                            if replies and replies != '' and 'data' in replies:
                                find_and_harvest_replies(replies['data']['children'])
                                
                find_and_harvest_replies(comments)
                
            else:
                print(f"Error fetching {url}: {response.status_code}")
        except Exception as e:
            print(f"Error processing {url}: {e}")

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
    print(f"Scan précis terminé. Réponses directes trouvées : {len(res['direct_replies'])}")
