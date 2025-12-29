#!/usr/bin/env python3
"""Domain-specific technology analyzer."""

DOMAINS = {
    "fintech": ["payments", "security", "compliance", "banking"],
    "healthcare": ["ehr", "fhir", "hipaa", "medical"],
    "ecommerce": ["cart", "checkout", "inventory", "shipping"],
}

def analyze_domain(keywords: list) -> str:
    """Identify domain from keywords."""
    scores = {}
    for domain, domain_keywords in DOMAINS.items():
        score = sum(1 for kw in keywords if kw.lower() in domain_keywords)
        if score > 0:
            scores[domain] = score

    if not scores:
        return "general"
    return max(scores, key=scores.get)

if __name__ == "__main__":
    keywords = ["payments", "security", "banking"]
    print(f"Domain: {analyze_domain(keywords)}")
