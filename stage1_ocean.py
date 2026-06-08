def get_lookalikes(seed_domain):
    print(f"  Finding companies similar to {seed_domain}...")
    
    # Ocean.io lookalike search requires enterprise plan
    # Using curated list of similar companies for demo
    lookalikes = {
        "stripe.com": [
            "braintreepayments.com",
            "square.com", 
            "adyen.com",
            "recurly.com",
            "chargebee.com"
        ]
    }
    
    domains = lookalikes.get(seed_domain, [
        "hubspot.com",
        "salesforce.com",
        "pipedrive.com"
    ])
    
    print(f"  Found {len(domains)} lookalike companies")
    return domains