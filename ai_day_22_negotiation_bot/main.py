import random

class NegotiationBot:
    def __init__(self, product, list_price, floor_price):
        self.product     = product
        self.list_price  = list_price
        self.floor_price = floor_price
        self.current     = list_price
        self.rounds      = 0
        self.max_rounds  = 4
        self.patience    = 3

    def respond(self, offer):
        self.rounds += 1
        offer = float(offer)
        if offer >= self.current:
            return "accept", f"Deal! I accept RM{offer:.0f} for the {self.product}. Thank you! 🤝"
        if offer < self.floor_price * 0.8:
            return "reject", f"That's way too low! The minimum I can go is around RM{self.floor_price:.0f}."
        gap      = self.current - offer
        concede  = min(gap * 0.4, (self.current - self.floor_price) * 0.5)
        new_price = round(self.current - concede, -1)
        new_price = max(new_price, self.floor_price)
        self.current = new_price
        if self.rounds >= self.max_rounds or new_price == self.floor_price:
            return "final", f"This is my final offer: RM{new_price:.0f}. I can't go lower than this."
        phrases = [
            f"Hmm, that's a bit low. How about we meet at RM{new_price:.0f}?",
            f"I appreciate the offer, but I can come down to RM{new_price:.0f}. What do you say?",
            f"Let me see what I can do... RM{new_price:.0f} is the best I can offer right now.",
            f"You drive a hard bargain! I can do RM{new_price:.0f} — deal?",
        ]
        return "counter", random.choice(phrases)

PRODUCTS = [
    ("Laptop",          4500, 3200),
    ("Smartphone",      2200, 1600),
    ("Mechanical Keyboard", 450, 300),
    ("Wireless Headphones", 350, 220),
    ("Monitor",         1200, 850),
]

def main():
    print("=== Price Negotiation Chatbot ===")
    print("Try to get the best price through negotiation!\n")
    print("Available items:")
    for i, (p, price, _) in enumerate(PRODUCTS, 1):
        print(f"  {i}. {p} — Listed at RM{price}")
    try:
        choice = int(input("\nChoose item (1-5): ")) - 1
        product, list_price, floor_price = PRODUCTS[choice]
    except:
        print("Invalid choice."); return
    bot = NegotiationBot(product, list_price, floor_price)
    print(f"\nSeller: Welcome! The {product} is RM{list_price}. Make me an offer.")
    while True:
        try:
            offer = input("\nYour offer (RM): ").strip().replace(",","")
            float(offer)
        except:
            print("Enter a valid number."); continue
        status, response = bot.respond(offer)
        print(f"\nSeller: {response}")
        if status == "accept":
            savings = list_price - float(offer)
            print(f"\n🎉 You saved RM{savings:.0f} ({savings/list_price*100:.0f}% off list price)!")
            break
        if status == "final":
            final = input("\nAccept final offer? (y/n): ").lower()
            if final == "y":
                print(f"\n🤝 Done! RM{bot.current:.0f} for the {product}.")
            else:
                print("\nNo deal. Come back when you're ready! 👋")
            break

if __name__ == "__main__":
    main()
