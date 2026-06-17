def bmi(weight_kg, height_m):
    return weight_kg / (height_m ** 2)

def category(bmi_val):
    if bmi_val < 18.5: return "Underweight", "🔵"
    if bmi_val < 25.0: return "Normal weight", "🟢"
    if bmi_val < 30.0: return "Overweight", "🟡"
    return "Obese", "🔴"

def ideal_weight(height_m):
    lo = 18.5 * (height_m ** 2)
    hi = 24.9 * (height_m ** 2)
    return lo, hi

def calories(weight_kg, height_cm, age, gender, activity):
    if gender.lower() == "m":
        bmr = 10*weight_kg + 6.25*height_cm - 5*age + 5
    else:
        bmr = 10*weight_kg + 6.25*height_cm - 5*age - 161
    factors = {"1":1.2,"2":1.375,"3":1.55,"4":1.725,"5":1.9}
    return bmr * float(factors.get(activity, 1.2))

def main():
    print("=== BMI & Health Calculator ===")
    while True:
        print("\n1. BMI Calculator  2. Ideal Weight  3. Daily Calories  4. Quit")
        c = input("Choice: ").strip()
        if c == "1":
            try:
                w = float(input("Weight (kg): "))
                h = float(input("Height (m, e.g. 1.72): "))
                b = bmi(w, h)
                cat, emoji = category(b)
                print(f"\n{emoji} BMI      : {b:.1f}")
                print(f"   Category : {cat}")
            except: print("Invalid input.")
        elif c == "2":
            try:
                h = float(input("Height (m): "))
                lo, hi = ideal_weight(h)
                print(f"\n✅ Ideal weight for {h}m: {lo:.1f} kg – {hi:.1f} kg")
            except: print("Invalid input.")
        elif c == "3":
            try:
                w = float(input("Weight (kg): "))
                h = float(input("Height (cm): "))
                a = int(input("Age: "))
                g = input("Gender (m/f): ")
                print("Activity: 1)Sedentary 2)Light 3)Moderate 4)Active 5)Very Active")
                act = input("Activity level: ")
                cal = calories(w, h, a, g, act)
                print(f"\n🔥 Maintenance calories: {cal:.0f} kcal/day")
                print(f"   Weight loss target  : {cal-500:.0f} kcal/day")
                print(f"   Weight gain target  : {cal+500:.0f} kcal/day")
            except: print("Invalid input.")
        elif c == "4":
            break

if __name__ == "__main__":
    main()
