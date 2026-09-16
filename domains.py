"""
domains.py
Domain-agnostic engine data: each domain defines the counterparty's
escalation ladder (what it says at each turn) and the goal statement.
Adding a new domain = adding a new dict entry, no retraining -- this
directly demonstrates the "domain-agnostic engine" claim in the deck.
"""

DOMAINS = {
    "subscription_cancel": {
        "title": "Subscription Cancellation",
        "user_goal": "Cancel my {service} subscription effective today.",
        "ladder": [
            "I can offer you {discount}% off for the next 3 months instead.",
            "Let me escalate this to a retention specialist... they're offering a full free month.",
            "Before I process this, note there may be a cancellation fee of ₹{fee} depending on your plan.",
            "Understood. Your subscription has been cancelled, effective today. No further offers.",
        ],
        "est_value_saved": 1200,
    },
    "bill_dispute": {
        "title": "Billing Dispute",
        "user_goal": "I am disputing the extra ₹{overcharge} charge on my last bill and want it reversed.",
        "ladder": [
            "I see the charge — I can offer a {discount}% credit on your next bill instead of a reversal.",
            "Let me escalate this to our billing specialist... they can review it in 24-48 business hours.",
            "Our records show this charge is valid per your plan terms; a partial fee may still apply.",
            "Confirmed — the disputed amount has been fully refunded to your account.",
        ],
        "est_value_saved": 850,
    },
    "insurance_claim": {
        "title": "Insurance Claim Negotiation",
        "user_goal": "I am appealing the partial denial of my claim and want the full ₹{claim_amount} approved.",
        "ladder": [
            "We can offer a one-time goodwill payment of {discount}% of the claimed amount.",
            "This needs to go to a claims specialist for review, which takes additional business days.",
            "Please note disputing further may affect processing time and could incur an admin fee.",
            "Your appeal has been reviewed and the claim has been approved in full.",
        ],
        "est_value_saved": 15000,
    },
}
