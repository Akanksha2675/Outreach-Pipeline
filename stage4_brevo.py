import requests
from config import BREVO_API_KEY

def send_emails(contacts):
    print(f"  Sending emails to {len(contacts)} contacts...")
    
    url = "https://api.brevo.com/v3/smtp/email"
    headers = {
        "api-key": BREVO_API_KEY,
        "Content-Type": "application/json"
    }
    
    sent = 0
    
    for contact in contacts:
        try:
            payload = {
                "sender": {
                    "name": "Akanksha Soni",
                    "email": "soniakanksha267@gmail.com"
                },
                "to": [{"email": contact["email"], "name": contact["name"]}],
                "subject": f"Quick question for you, {contact['name'].split()[0]}",
                "htmlContent": f"""
                <p>Hi {contact['name'].split()[0]},</p>
                
                <p>I came across {contact['company']} and was really impressed by what you're building.</p>
                
                <p>I'm reaching out because I think there's a genuine opportunity to work together. 
                Would you be open to a quick 15-minute call this week to explore it?</p>
                
                <p>Best,<br>Akanksha Soni</p>
                """
            }
            
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            sent += 1
            print(f"  Sent to {contact['name']} <{contact['email']}>")
        
        except Exception as e:
            print(f"  Failed to send to {contact.get('name')}: {e}")
            continue
    
    print(f"  Successfully sent {sent} emails")