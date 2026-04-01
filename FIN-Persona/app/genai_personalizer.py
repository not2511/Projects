import time
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

CHANNEL_STYLE = {
    "SMS":      "Max 2 short sentences. No emojis. Plain text only.",
    "Email":    "Max 3 sentences. Warm and professional. No bullet points. Must be complete.",
    "WhatsApp": "Max 2 sentences. Friendly tone. Exactly 1 emoji at the end only.",
    "Push":     "Max 8 words total. Action-oriented. No emoji."
}

def build_prompt(customer, segment, strategy):
    channel = customer["preferred_channel"]
    style = CHANNEL_STYLE.get(channel, "Short and clear")
    name = customer["name"].replace("_", " ")  # "Customer 5" not "Customer_5"

    return f"""You are a customer communication assistant for an Indian bank.
Write a personalized message for this customer.

Customer Profile:
- Name: {name}
- Age: {customer['age']}
- Monthly Income: ₹{customer['monthly_income']:,}
- Average Balance: ₹{customer['avg_balance']:,}
- Missed Payments: {customer['missed_payments']}
- Risk Score: {customer['risk_score']:.2f}
- Segment: {segment}
- Communication Goal: {strategy}
- Channel: {channel}

Style Instructions: {style}
Important rules:
- Use the customer's actual name, never placeholders
- Never sign off with a name, signature, or "regards"
- Never add "For more information" or "feel free to reach out"
- Write as an automated bank notification, not a human email
- WhatsApp: exactly 1 emoji only, at the very end

Write ONLY the message. Nothing else."""


def generate_message(customer, segment, strategy):
    prompt = build_prompt(customer, segment, strategy)

    start = time.time()
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=80,
        temperature=0.7,
        timeout=10,
    )
    latency = time.time() - start

    message = response.choices[0].message.content.strip()
    return message, latency


if __name__ == "__main__":
    from data_generator import generate_customers
    from feature_engineering import engineer_features
    from segmentation import segment_customers

    df = generate_customers()
    df = engineer_features(df)
    df, _ = segment_customers(df)

    # Test
    print(" Testing GenAI personalization\n")
    print("=" * 60)

    for segment in df["segment"].unique():
        customer = df[df["segment"] == segment].iloc[0]
        message, latency = generate_message(
            customer, customer["segment"], customer["strategy"]
        )
        print(f"Segment:  {segment}")
        print(f"Channel:  {customer['preferred_channel']}")
        print(f"Message:  {message}")
        print(f"Latency:  {latency:.2f}s")
        print("-" * 60)