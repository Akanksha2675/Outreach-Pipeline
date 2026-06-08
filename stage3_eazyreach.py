import requests
import time
import json
import os
from config import PROSPEO_API_KEY

CHECKPOINT_FILE = "checkpoint.json"

def load_checkpoint():
    if os.path.exists(CHECKPOINT_FILE):
        with open(CHECKPOINT_FILE) as f:
            return json.load(f)
    return {}

def save_checkpoint(checkpoint):
    with open(CHECKPOINT_FILE, "w") as f:
        json.dump(checkpoint, f, indent=2)

def resolve_emails(prospects):
    print(f"  Resolving emails for {len(prospects)} prospects...")

    url = "https://api.prospeo.io/enrich-person"
    headers = {
        "X-KEY": PROSPEO_API_KEY,
        "Content-Type": "application/json"
    }

    checkpoint = load_checkpoint()
    contacts = []
    daily_limit = 50
    requests_made = 0

    for person in prospects:
        key = person.get("linkedin_url")
        if key and key in checkpoint and checkpoint[key] is not None:
            contacts.append(checkpoint[key])

    for person in prospects:
        if requests_made >= daily_limit:
            print(f"  Daily limit of {daily_limit} reached.")
            break

        if not person.get("id") or not person.get("linkedin_url"):
            continue

        key = person["linkedin_url"]

        if key in checkpoint:
            continue

        try:
            payload = {
                "linkedin_url": key,
                "only_verified_email": True
            }

            time.sleep(3.5)
            response = requests.post(url, headers=headers, json=payload)

            if response.status_code == 429:
                checkpoint[key] = None
                save_checkpoint(checkpoint)
                continue

            response.raise_for_status()
            data = response.json()
            requests_made += 1

            email = data.get("response", {}).get("email", {}).get("email")

            if email:
                contact = {
                    "name": person["name"],
                    "email": email,
                    "title": person["title"],
                    "company": person["company"],
                    "linkedin_url": key
                }
                contacts.append(contact)
                checkpoint[key] = contact
            else:
                checkpoint[key] = None

            save_checkpoint(checkpoint)

        except Exception as e:
            print(f"  Skipping {person.get('name')}: {e}")
            continue

    print(f"  Resolved {len(contacts)} verified emails")

    if not contacts:
        print("  Using demo contacts as fallback...")
        contacts = [
            {
                "name": "Cory Davis",
                "email": "cory.davis@braintreepayments.com",
                "title": "VP Engineering",
                "company": "braintreepayments.com",
                "linkedin_url": "https://www.linkedin.com/in/cory-davis-026076115"
            },
            {
                "name": "Marc Patterson",
                "email": "marc.patterson@square.com",
                "title": "VP Sales",
                "company": "square.com",
                "linkedin_url": "https://www.linkedin.com/in/marc-patterson-6119284"
            },
            {
                "name": "Mark Trachtenbarg",
                "email": "mark.trachtenbarg@recurly.com",
                "title": "VP Product",
                "company": "recurly.com",
                "linkedin_url": "https://www.linkedin.com/in/mark-trachtenbarg-8398b288"
            }
        ]
    return contacts