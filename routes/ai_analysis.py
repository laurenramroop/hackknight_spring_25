import os
import requests
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Keys
NESSIE_API_KEY = os.getenv("API_KEY")
NESSIE_BASE_URL = os.getenv("BASE_URL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")



# Set up OpenAI API client
client = openai.OpenAI(api_key=OPENAI_API_KEY)

# Hardcoded account ID (for testing/demo)
ACCOUNT_ID = "67cd8d279683f20dd518f83a"

# Function to get account balance
def get_account_balance(account_id):
    url = f"{NESSIE_BASE_URL}/accounts/{account_id}?key={NESSIE_API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        account_data = response.json()
        return account_data.get("balance", 0)  # Default to 0 if missing
    else:
        print(f"Error fetching account balance: {response.json()}")
        return None

# Function to determine if the purchase is a WANT or NEED
def categorize_purchase(item_name):
    needs = ["groceries", "rent", "utilities", "medical", "insurance"]
    wants = ["gaming", "fast food", "shoes", "designer", "luxury", "iphone"]

    item_name_lower = item_name.lower()

    for need in needs:
        if need in item_name_lower:
            return "NEED"
    
    for want in wants:
        if want in item_name_lower:
            return "WANT"
    
    return "UNKNOWN"

# Function to analyze purchase
def analyze_purchase(item, cost, roast_level):
    balance = get_account_balance(ACCOUNT_ID)

    if balance is None:
        return "Error retrieving balance. Try again later."

    # Check if the purchase exceeds the available balance
    if balance - cost < 0:
        financial_status = "BROKE AF (Overdraft)"
    elif (cost / balance) * 100 > 50:
        financial_status = "Big Spending (50%+ of balance)"
    else:
        financial_status = "You're financially safe... for now"

    # Calculate percentage of balance used
    percent_spent = (cost / balance) * 100

    # Determine if the purchase is a WANT or NEED
    category = categorize_purchase(item)

    # Generate the AI response
    return generate_ai_response(item, cost, financial_status, percent_spent, category, roast_level)

# Function to generate an AI response using OpenAI
def generate_ai_response(item, cost, financial_status, percent_spent, category, roast_level):
    roast_texts = {
        1: "That’s a reasonable purchase. Financially valid. Good job.",
        2: "Hmmm… Are you sure this is necessary? Might be time to budget smarter.",
        3: "Logically speaking, this purchase is... questionable.",
        4: "This is a certified ‘bad financial decision’ moment. Think again.",
    }

    gen_z_slurs = [
        "Bro, your wallet is on life support. ",
        "You’re speedrunning bankruptcy.",
        "Nah, you’re actually committing financial fraud against yourself. ",
        "Hope you enjoy eating air sandwiches for the next month. ",
    ]

    # Select roast level and slang response
    roast_intro = roast_texts.get(roast_level, "Are you sure about this purchase?")
    slang_roast = gen_z_slurs[min(roast_level - 1, len(gen_z_slurs) - 1)]

    # OpenAI API Call (New Syntax)
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a funny financial advisor with Gen Z/Millennial humor."},
                {"role": "user", "content": f"I want to buy {item} for ${cost}. My financial status is: {financial_status}. "
                                            f"This will use {percent_spent:.2f}% of my balance. Category: {category}. "
                                            f"Roast me at level {roast_level} (1-5)."}
            ],
            temperature=0.7
        )
        ai_response = response.choices[0].message.content.strip()
    except Exception as e:
        ai_response = f"Error generating AI response: {str(e)}"

    return f"{roast_intro}\n\n{slang_roast}\n\n{ai_response}"

# Example usage
if __name__ == "__main__":
    item = input("Enter item you want to buy: ")
    cost = float(input("Enter cost: "))
    roast_level = int(input("Enter roast level (1-5): "))

    response = analyze_purchase(item, cost, roast_level)
    print("\nAI Analysis:\n", response)
