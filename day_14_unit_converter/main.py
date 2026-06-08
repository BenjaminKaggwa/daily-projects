def length(val, frm, to):
    to_m = {"km":1000,"m":1,"cm":0.01,"mm":0.001,"mile":1609.34,"yard":0.9144,"foot":0.3048,"inch":0.0254}
    return val * to_m[frm] / to_m[to]

def weight(val, frm, to):
    to_kg = {"kg":1,"g":0.001,"mg":0.000001,"lb":0.453592,"oz":0.0283495,"tonne":1000}
    return val * to_kg[frm] / to_kg[to]

def temperature(val, frm, to):
    if frm == to: return val
    if frm == "C":
        return val * 9/5 + 32 if to == "F" else val + 273.15
    if frm == "F":
        return (val - 32) * 5/9 if to == "C" else (val - 32) * 5/9 + 273.15
    if frm == "K":
        return val - 273.15 if to == "C" else (val - 273.15) * 9/5 + 32

def speed(val, frm, to):
    to_ms = {"m/s":1,"km/h":1/3.6,"mph":0.44704,"knot":0.514444}
    return val * to_ms[frm] / to_ms[to]

MENUS = {
    "1": ("Length",      ["km","m","cm","mm","mile","yard","foot","inch"], length),
    "2": ("Weight",      ["kg","g","mg","lb","oz","tonne"],                weight),
    "3": ("Temperature", ["C","F","K"],                                    temperature),
    "4": ("Speed",       ["m/s","km/h","mph","knot"],                      speed),
}

def main():
    print("=== Unit Converter ===")
    while True:
        print("\n1. Length  2. Weight  3. Temperature  4. Speed  5. Quit")
        c = input("Choice: ").strip()
        if c == "5": break
        if c not in MENUS:
            print("Invalid."); continue
        name, units, fn = MENUS[c]
        print(f"\n{name} units: {', '.join(units)}")
        try:
            val = float(input("Value: "))
            frm = input("From unit: ").strip()
            to  = input("To unit: ").strip()
            if frm not in units or to not in units:
                print("Invalid unit."); continue
            result = fn(val, frm, to)
            print(f"\n✅ {val} {frm} = {result:.6g} {to}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
