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
    "gym_membership": {
        "title": "Gym Membership Cancellation",
        "user_goal": "Cancel my gym membership effective today, no further billing.",
        "ladder": [
            "As a valued member, we can offer {discount}% off if you downgrade instead of cancelling.",
            "Let me escalate this to our membership specialist — they may offer a free month to stay.",
            "Note that early cancellation may incur a fee of ₹{fee} per your contract terms.",
            "Confirmed — your membership has been cancelled effective today, no further charges.",
        ],
        "est_value_saved": 900,
    },
    "flight_refund": {
        "title": "Flight Cancellation Refund",
        "user_goal": "I want a full refund of ₹{claim_amount} for my cancelled flight, not a travel credit.",
        "ladder": [
            "We can offer travel credit worth {discount}% extra instead of a cash refund.",
            "Let me escalate this to our refunds specialist for review, which takes a few business days.",
            "Per our fare terms and conditions, a processing fee of ₹{fee} may apply to cash refunds.",
            "Confirmed — the full amount has been refunded to your original payment method.",
        ],
        "est_value_saved": 8000,
    },
    "landlord_deposit": {
        "title": "Rental Deposit Return",
        "user_goal": "I want my full ₹{claim_amount} security deposit returned with no deductions.",
        "ladder": [
            "We can offer to credit {discount}% of the deposit now and review the rest later.",
            "Let me escalate this to the property manager for a walkthrough review.",
            "Per the lease terms and conditions, cleaning charges of ₹{fee} may apply.",
            "Confirmed — your full deposit has been approved for return.",
        ],
        "est_value_saved": 20000,
    },
    "phone_plan_downgrade": {
        "title": "Phone Plan Downgrade Dispute",
        "user_goal": "Downgrade my plan today with no penalty, as originally advertised.",
        "ladder": [
            "We can offer {discount}% off your current plan instead of downgrading.",
            "Let me escalate this to a plans specialist — they're offering a loyalty bonus to stay.",
            "Note that changing plans mid-cycle may incur a fee of ₹{fee}.",
            "Understood — your plan has been downgraded today, no further offers.",
        ],
        "est_value_saved": 600,
    },
    "warranty_claim": {
        "title": "Product Warranty Claim",
        "user_goal": "I want a full replacement covered under warranty, not a paid repair.",
        "ladder": [
            "We can offer a {discount}% discount on a paid repair instead of a replacement.",
            "Let me escalate this to our warranty specialist for further review.",
            "Please note you may incur a service fee of ₹{fee} if the damage is found to be accidental.",
            "Confirmed — a full replacement has been approved under warranty.",
        ],
        "est_value_saved": 5000,
    },
    "hotel_refund": {
        "title": "Hotel Booking Refund",
        "user_goal": "I want a full refund of ₹{claim_amount} for my cancelled hotel stay.",
        "ladder": [
            "We can offer {discount}% off your next stay instead of a refund.",
            "Let me escalate this to our reservations specialist for a manual review.",
            "Per our booking terms and conditions, a cancellation fee of ₹{fee} may apply.",
            "Confirmed — your stay has been fully refunded to your original payment method.",
        ],
        "est_value_saved": 4500,
    },
    "loan_prepayment_penalty": {
        "title": "Loan Prepayment Penalty Waiver",
        "user_goal": "Waive the prepayment penalty of ₹{fee} on my loan foreclosure.",
        "ladder": [
            "We can offer a {discount}% reduction on the penalty instead of a full waiver.",
            "Let me escalate this to our loans specialist for a case-by-case review.",
            "Per your loan agreement terms and conditions, this penalty is valid as charged.",
            "Confirmed — the prepayment fee has been fully waived, no further action needed.",
        ],
        "est_value_saved": 7000,
    },
    "credit_card_annual_fee": {
        "title": "Credit Card Annual Fee Waiver",
        "user_goal": "Waive my ₹{fee} annual fee for this year, or I will close the card.",
        "ladder": [
            "As a valued customer, we can offer {discount}% off the annual fee instead of a full waiver.",
            "Let me escalate this to a retention specialist — they may offer bonus reward points to stay.",
            "Per your cardmember terms and conditions, the annual fee is non-refundable after 30 days.",
            "Confirmed — your annual fee has been fully waived for this year.",
        ],
        "est_value_saved": 2000,
    },
    "internet_downtime_credit": {
        "title": "Internet Downtime Bill Credit",
        "user_goal": "Credit my bill in full for {service} being down for 5 days last month.",
        "ladder": [
            "We can offer a {discount}% credit on your next bill for the downtime.",
            "Let me escalate this to our network specialist to verify the outage on our end.",
            "Note that you may incur a technician visit fee of ₹{fee} if the issue is on your side.",
            "Confirmed — your bill has been fully credited for the downtime period.",
        ],
        "est_value_saved": 700,
    },
    "rental_car_damage": {
        "title": "Rental Car Damage Dispute",
        "user_goal": "I dispute the ₹{overcharge} damage charge — the damage was pre-existing.",
        "ladder": [
            "We can offer a {discount}% reduction on the damage charge as a goodwill gesture.",
            "Let me escalate this to our claims specialist to review the pickup inspection photos.",
            "Per our rental terms and conditions, the charge stands unless you provide documentation.",
            "Confirmed — the damage charge has been fully reversed based on your documentation.",
        ],
        "est_value_saved": 3500,
    },
    "ecommerce_return": {
        "title": "E-commerce Return Refund",
        "user_goal": "I want a full refund of ₹{claim_amount} for the defective item I returned.",
        "ladder": [
            "We can offer store credit worth {discount}% extra instead of a cash refund.",
            "Let me escalate this to our returns specialist to verify the item condition.",
            "Note that a restocking fee of ₹{fee} may apply per our return policy terms and conditions.",
            "Confirmed — the full amount has been refunded to your original payment method.",
        ],
        "est_value_saved": 1500,
    },
    "medical_bill": {
        "title": "Medical Bill Negotiation",
        "user_goal": "I am disputing the ₹{overcharge} out-of-network charge and want it reversed.",
        "ladder": [
            "We can offer a {discount}% discount on the disputed charge as a courtesy adjustment.",
            "Let me escalate this to our billing specialist for an insurance re-verification.",
            "Per your plan terms and conditions, out-of-network charges are billed at full rate.",
            "Confirmed — the disputed charge has been fully reversed on your account.",
        ],
        "est_value_saved": 6000,
    },
    "late_delivery": {
        "title": "Late Delivery Compensation",
        "user_goal": "I want full compensation of ₹{claim_amount} for my order arriving 10 days late.",
        "ladder": [
            "We can offer a {discount}% discount coupon for a future order instead of cash compensation.",
            "Let me escalate this to our logistics specialist to confirm the delay reason.",
            "Please note compensation claims are reviewed within a few business days.",
            "Confirmed — full compensation has been approved and refunded to your account.",
        ],
        "est_value_saved": 1000,
    },
    "software_subscription_refund": {
        "title": "Software Subscription Refund",
        "user_goal": "I want a full refund of ₹{fee} — I was charged after cancelling.",
        "ladder": [
            "We can offer {discount}% off your next renewal instead of a refund.",
            "Let me escalate this to our billing specialist to verify your cancellation date.",
            "Per our terms and conditions, refunds are only issued within 7 days of the charge.",
            "Confirmed — the charge has been fully refunded to your original payment method.",
        ],
        "est_value_saved": 800,
    },
    "parking_fine_appeal": {
        "title": "Parking Fine Appeal",
        "user_goal": "I am appealing the ₹{fee} parking fine — the signage was missing.",
        "ladder": [
            "We can offer a {discount}% discount on the fine as a one-time courtesy.",
            "Let me escalate this to our appeals specialist to review the site photos.",
            "Per municipal terms and conditions, fines are valid unless overturned by appeal.",
            "Confirmed — your fine has been fully waived following the appeal review.",
        ],
        "est_value_saved": 500,
    },
    "utility_bill_dispute": {
        "title": "Utility Bill Dispute",
        "user_goal": "I am disputing an unusually high charge of ₹{overcharge} on my utility bill.",
        "ladder": [
            "We can offer a {discount}% credit on your next bill instead of a full reversal.",
            "Let me escalate this to our metering specialist to check for a faulty meter reading.",
            "Per your service terms and conditions, billed usage is presumed accurate unless disputed in writing.",
            "Confirmed — the disputed amount has been fully reversed on your account.",
        ],
        "est_value_saved": 1100,
    },
    "event_ticket_refund": {
        "title": "Event Ticket Refund",
        "user_goal": "I want a full refund of ₹{claim_amount} for the cancelled event.",
        "ladder": [
            "We can offer a {discount}% bonus credit toward a future event instead of a refund.",
            "Let me escalate this to our ticketing specialist for manual processing.",
            "Per our ticketing terms and conditions, a processing fee of ₹{fee} may apply to refunds.",
            "Confirmed — your ticket has been fully refunded to your original payment method.",
        ],
        "est_value_saved": 2500,
    },
}
