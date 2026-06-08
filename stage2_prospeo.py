import requests
import time
from config import PROSPEO_API_KEY

def get_contacts(domains):
    print(f"  Finding decision-makers across {len(domains)} companies...")
    
    url = "https://api.prospeo.io/search-person"
    headers = {
        "X-KEY": PROSPEO_API_KEY,
        "Content-Type": "application/json"
    }
    
    all_prospects = []
    
    for domain in domains:
        try:
            payload = {
                "page": 1,
                "filters": {
                    "company": {
                        "websites": {
                            "include": [domain]
                        }
                    }
                }
            }
            
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            
            people = data.get("results", [])
            for person in people:
                p = person.get("person", {})
                all_prospects.append({
                    "id": p.get("person_id"),
                    "name": p.get("full_name", ""),
                    "title": p.get("current_job_title", ""),
                    "company": domain,
                    "linkedin_url": p.get("linkedin_url", "")
            })
            
            time.sleep(3)
        
        except Exception as e:
            print(f"  Skipping {domain}: {e}")
            continue
    
    # Deduplicate by linkedin_url
    seen = set()
    unique = []
    for p in all_prospects:
        key = p.get("linkedin_url") or p.get("id")
        if key and key not in seen:
            seen.add(key)
            unique.append(p)
    
    print(f"  Found {len(unique)} decision-makers")
    return unique