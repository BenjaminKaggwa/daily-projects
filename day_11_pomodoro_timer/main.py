import time

def countdown(seconds, label):
    print(f"\n⏱  {label}")
    while seconds:
        m, s = divmod(seconds, 60)
        print(f"  {m:02d}:{s:02d}", end="\r")
        time.sleep(1)
        seconds -= 1
    print("  00:00 ✅")

def main():
    print("=== Pomodoro Timer ===")
    session = 1
    while True:
        print(f"\n--- Session {session} ---")
        input("Press Enter to start 25-minute work session...")
        countdown(25 * 60, "Work Session")
        print("\n🔔 Work done! Time for a break.")
        if session % 4 == 0:
            input("Press Enter to start 15-minute long break...")
            countdown(15 * 60, "Long Break")
        else:
            input("Press Enter to start 5-minute short break...")
            countdown(5 * 60, "Short Break")
        print("\n🔔 Break over!")
        session += 1
        again = input("Continue? (y/n): ")
        if again.lower() != "y":
            print(f"\nCompleted {session-1} pomodoro(s). Great work!")
            break

if __name__ == "__main__":
    main()
