# Assume there are some blogs that are no free, customers must pay to unlock them 
# So I develop this payment serive to create order, call Paypal API to complete txn, and then return status 

from flask import request, abort, jsonify
from flaskblog import app, engine 
from sqlalchemy import text 
from datetime import datetime, timezone

# helper function
def payment_row_to_dict(row):
    m = row._mapping 
    return {
        "id": m["id"],
        "user_id": m["user_id"],
        "amount_cents": m["amount_cents"],
        "currency": m["currency"],
        "status": m["status"],
        "description": m["description"],
        "created_at": m["created_at"],
        "updated_at": m["updated_at"],
    }

#########Create Payment######
"""
Frontend send request:

POST /api/payments
Content-Type: application/json

{
  "user_id": 1,
  "amount_cents": 500,
  "currency": "USD",
  "description": "Unlock premium post #42"
}

Backend create a record of txn and return response 
{
  "id": 10,
  "user_id": 1,
  "amount_cents": 500,
  "currency": "USD",
  "status": "created",
  "description": "Unlock premium post #42",
  "created_at": "2025-11-17T12:00:00Z",
  "updated_at": "2025-11-17T12:00:00Z"
}
"""
@app.route("/api/payments", methods=["POST"])
def create_payment():
    data = request.get_json(silent=True) or {}
    user_id = data.get("user_id")
    amount_cents = data.get("amount_cents")
    currency = data.get("currency", "USD")
    description = data.get("description", "")

    if not user_id or not amount_cents:
        return jsonify({"error": "user_id and amount_cents are required"}), 400

    now = datetime.now(timezone.utc).isoformat()  # covert utc timestamp to string 

    with engine.begin() as conn:
        result = conn.execute(
            text("""
                    INSERT INTO payment (user_id, amount_cents, currency, status, description, created_at, updated_at)
                    VALUES (:user_id, :amount_cents, :currency, :status, :description, :created_at, :updated_at)
                    RETURNING id, user_id, amount_cents, currency, status, description, created_at, updated_at
                """),
                {
                    "user_id": user_id,
                    "amount_cents": amount_cents,
                    "currency": currency,
                    "status": "created",
                    "description": description,
                    "created_at" : now,
                    "updated_at" : now
                }
        )
        row = result.first()
    
    return jsonify(payment_row_to_dict(row)), 200 


#########CALL PayPal SDK######
"""
Call PayPal API to establish an order:  
POST https://api.paypal.com/v2/checkout/orders

or sudo code: 
paypal_response = call_paypal_create_order(
    amount=500,
    currency="USD",
    payment_id = 1208098098 # this is the one we created
    return_url="https://yourapp.com/pay/return",
    cancel_url="https://yourapp.com/pay/cancel"
)

Paypal reposes with redirect url/token:
{
  "payment_id": 99,
  "paypal_order_id": "5TR84...",  # this the one paypal created 
  "redirect_url": "https://paypal.com/checkout?token=xxx"
}
"""

#########Redirect to PayPal######
"""
Frontend may be polling (or retry) this redirect url/token, and sever then response url and payment_id back to frontend
Then customer will be redirected to PayPal. Customer will enter credentials
Then Paypal is responsible for authorization, money transfer, fraud.  
"""

######### Webhook, Paypal inform status ######
"""
Webhook essentially is a reverse API. Asynchronous. 
Paypal send request to my backend server:

POST https://yourserver.com/webhooks/paypal 
Content-Type: application/json

{
  "event": "PAYMENT.CAPTURE.COMPLETED",
  "order_id": "5TR84...",
  "amount": 500,
  "currency": "USD",
  "status": "COMPLETED"
}

Sever then map request with local payment id and update status accordingly 
"""
@app.route("/webhook/paypal", methods=["POST"])
def paypal_webhook():
    event = request.get_json(silent=True) or {}

    # assume request body include fields like resource and event type
    paypal_order_id  = event.get("resource", {}).get("id")
    event_type = event.get("event_type")  # e.g. "CHECKOUT.ORDER.APPROVED"

    if not paypal_order_id:
        return jsonify({"error": "missing paypal_order_id"}), 400
    
    # map order id to local payment id and status
    if event_type == "CHECKOUT.ORDER.APPROVED":
        new_status = "succeeded"
    elif event_type == "CHECKOUT.ORDER.CANCELLED":
        new_status = "failed"
    else:
        # temporarily ignore other type
        return jsonify({"status": "ignored"}), 200
    
    now = datetime.now(timezone.utc).isoformat()
    with engine.begin() as conn:
        result = conn.execute(
            text("""
                SELECT * FROM payment WHERE paypal_order_id = :oid; 
                """),
            {"oid": paypal_order_id}
        ).first()

        if result is None:
            # if not found, keep a log record and return 200 to avoid Paypal retry
            return jsonify({"status": "payment_not_found"}), 200
        
        conn.execute(
            text("""
                UPDATE payment
                SET status = :status, updated_at = :updated_at            
                WHERE paypal_order_id = :oid
                """),
            {
                "status": new_status,
                "updated_at": now,
                "oid": paypal_order_id
            }
        )
    return jsonify({"status": "ok"}), 200
 
######### Frontend check payment status ######
@app.route("/api/payments/<int:payment_id>", methods=["GET"])
def get_payment(payment_id):
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM payment WHERE payment_id =:payment_id"), {"payment_id":payment_id}).first()

        if not result:
            return jsonify({"error": "payment not found"}), 404
    
    return jsonify(payment_row_to_dict(result)), 200 

"""
sudo code of frontend polling request

async def pollPaymentStatus(payment_id):
    while True:
        const res = await fetch('/api/payments/${paymentId}')
        const data = await res.json()

        if data.status == "Succeeded":
            print("Payment Succeeded, blog post is unlocked, thank you.")
            break
        elif data.status == "failed":
            print("Payment failed, please retry later.")
            break

        await sleep(2000)  # every 2 second 
"""

