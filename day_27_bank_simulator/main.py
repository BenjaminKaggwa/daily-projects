from datetime import datetime

class BankAccount:
    def __init__(self, owner, account_number, account_type="Savings"):
        self.owner          = owner
        self.account_number = account_number
        self.account_type   = account_type
        self._balance       = 0.0
        self._transactions  = []

    def _log(self, kind, amount, note=""):
        self._transactions.append({
            "type": kind, "amount": amount,
            "balance": self._balance,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "note": note
        })

    def deposit(self, amount, note=""):
        if amount <= 0: raise ValueError("Amount must be positive")
        self._balance += amount
        self._log("Deposit", amount, note)
        print(f"✅ Deposited RM{amount:.2f}. New balance: RM{self._balance:.2f}")

    def withdraw(self, amount, note=""):
        if amount <= 0: raise ValueError("Amount must be positive")
        if amount > self._balance: raise ValueError("Insufficient funds")
        self._balance -= amount
        self._log("Withdrawal", amount, note)
        print(f"✅ Withdrew RM{amount:.2f}. New balance: RM{self._balance:.2f}")

    def transfer(self, target, amount):
        self.withdraw(amount, f"Transfer to {target.owner}")
        target.deposit(amount, f"Transfer from {self.owner}")
        print(f"✅ Transferred RM{amount:.2f} to {target.owner}")

    @property
    def balance(self):
        return self._balance

    def statement(self):
        print(f"\n{'='*55}")
        print(f"  {self.owner} — {self.account_type} Account #{self.account_number}")
        print(f"  Balance: RM{self._balance:.2f}")
        print(f"{'='*55}")
        if not self._transactions:
            print("  No transactions yet.")
        else:
            print(f"  {'Date':<18} {'Type':<12} {'Amount':>10} {'Balance':>10}  Note")
            print(f"  {'-'*50}")
            for t in self._transactions[-10:]:
                print(f"  {t['time']:<18} {t['type']:<12} RM{t['amount']:>8.2f} RM{t['balance']:>8.2f}  {t['note']}")
        print("="*55)

def main():
    print("=== Bank Account Simulator ===")
    name  = input("Account holder name: ")
    acno  = input("Account number (e.g. 1234-5678): ")
    acc   = BankAccount(name, acno)
    acc2  = None
    while True:
        print("\n1.Deposit  2.Withdraw  3.Statement  4.Open 2nd Account  5.Transfer  6.Quit")
        c = input("Choice: ").strip()
        try:
            if c == "1":
                a = float(input("Amount (RM): "))
                n = input("Note (optional): ")
                acc.deposit(a, n)
            elif c == "2":
                a = float(input("Amount (RM): "))
                n = input("Note (optional): ")
                acc.withdraw(a, n)
            elif c == "3":
                acc.statement()
            elif c == "4":
                n2   = input("2nd account holder: ")
                acno2 = input("2nd account number: ")
                acc2 = BankAccount(n2, acno2)
                print(f"Account for {n2} created.")
            elif c == "5":
                if not acc2: print("Open a 2nd account first."); continue
                a = float(input("Transfer amount (RM): "))
                acc.transfer(acc2, a)
            elif c == "6":
                break
        except ValueError as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
