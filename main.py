import sys
from stage1_ocean import get_lookalikes
from stage2_prospeo import get_contacts
from stage3_eazyreach import resolve_emails
from stage4_brevo import send_emails

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <seed_domain>")
        print("Example: python main.py stripe.com")
        sys.exit(1)
    
    seed_domain = sys.argv[1]
    print(f"\n=== Outreach Pipeline Starting ===")
    print(f"Seed domain: {seed_domain}\n")

    print("[1/4] Finding lookalike companies...")
    domains = get_lookalikes(seed_domain)
    if not domains:
        print("No lookalike companies found. Exiting.")
        sys.exit(1)

    print(f"\n[2/4] Finding decision-makers...")
    prospects = get_contacts(domains)
    if not prospects:
        print("No prospects found. Exiting.")
        sys.exit(1)

    print(f"\n[3/4] Resolving verified emails...")
    contacts = resolve_emails(prospects)
    if not contacts:
        print("No verified emails found. Exiting.")
        sys.exit(1)

    print(f"\n=== READY TO SEND ===")
    print(f"Recipients: {len(contacts)}")
    for c in contacts:
        print(f"  {c['name']} <{c['email']}> — {c['company']} — {c['title']}")
    
    confirm = input("\nSend emails? (yes/no): ")
    if confirm.lower() != "yes":
        print("Aborted. No emails sent.")
        sys.exit(0)

    print(f"\n[4/4] Sending emails...")
    send_emails(contacts)

    print(f"\n=== Pipeline Complete ===")

if __name__ == "__main__":
    main()