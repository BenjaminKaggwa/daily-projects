import requests

BASE_URL = "https://open.er-api.com/v6/latest/"

def get_rates(base="USD"):
    try:
        r = requests.get(BASE_URL + base, timeout=5)
        data = r.json()
        if data.get("result") == "success":
            return data["rates"], data["time_last_update_utc"]
        return None, None
    except Exception as e:
        print(f"Error fetching rates: {e}")
        return None, None

def convert(amount, frm, to, rates):
    if frm not in rates or to not in rates:
        return None
    usd_amount = amount / rates[frm] if frm != "USD" else amount
    result = usd_amount * rates[to]
    return result

def main():
    print("=== Currency Converter ===")
    print("Fetching live exchange rates...")
    rates, updated = get_rates("USD")
    if not rates:
        print("Could not fetch rates. Check your internet connection."); return
    print(f"Rates updated: {updated}")
    print(f"Supported currencies: {', '.join(sorted(rates.keys()))}")
    while True:
        print("\n1. Convert  2. List currencies  3. Quit")
        c = input("Choice: ").strip()
        if c == "1":
            try:
                amt  = float(input("Amount: "))
                frm  = input("From currency (e.g. USD): ").upper()
                to   = input("To currency (e.g. MYR): ").upper()
                result = convert(amt, frm, to, rates)
                if result is None: print("Invalid currency code.")
                else: print(f"\n💱 {amt} {frm} = {result:.4f} {to}")
            except ValueError: print("Invalid amount.")
        elif c == "2":
            cols = sorted(rates.keys())
            for i in range(0, len(cols), 8):
                print("  " + "  ".join(f"{x:<5}" for x in cols[i:i+8]))
        elif c == "3":
            break

if __name__ == "__main__":
    main()
