
"""
Author:         Jake Bredice
Date:           11-4
Assignment:     Lab 08
Course:         CPSC1051
Lab Section:    SECTION 101

CODE DESCRIPTION:
Icecream ordering system

"""
from icecream_db import initialize_db, save_order, get_next_order_number

# ----------------- Topping Class -----------------
class Topping:
    def __init__(self):
        self.type = ""
        self.cost = 0.0

    def validate_topping(self, type):
        return type.lower() in ["sprinkles", "gummy bears", "oreos", "caramel",
                                "chocolate chips", "peanuts", "done"]

    def set_type(self, type):
        self.type = type.lower()
        if self.type == "sprinkles": self.cost = 0.15
        elif self.type == "gummy bears": self.cost = 0.45
        elif self.type == "oreos": self.cost = 0.38
        elif self.type == "caramel": self.cost = 0.50
        elif self.type == "chocolate chips": self.cost = 0.40
        elif self.type == "peanuts": self.cost = 0.55

    def get_type(self):
        return self.type

    def get_cost(self):
        return self.cost

# ----------------- IceCream Class -----------------
class IceCream:
    def __init__(self):
        self.flavor = ""
        self.num_scoops = 0
        self.price_per_scoop = 0.0
        self.is_deluxe_brand = False
        self.toppings = []

    def validate_flavor(self, flavor):
        return flavor.lower() in ["vanilla", "chocolate", "strawberry", "mint",
                                  "cookies and cream", "rocky road", "coffee",
                                  "peppermint", "pumpkin", "mango", "strawberry cheesecake"]

    def set_flavor(self, flavor):
        self.flavor = flavor.lower()
        # Base pricing scheme
        flavor_prices = {
            "vanilla": 1.05, "chocolate": 1.12, "strawberry": 1.32,
            "mint": 1.20, "cookies and cream": 1.50, "rocky road": 1.60,
            "coffee": 1.40, "peppermint": 1.45, "pumpkin": 1.50,
            "mango": 1.55, "strawberry cheesecake": 1.60
        }
        self.price_per_scoop = flavor_prices.get(self.flavor, 1.50)

    def set_num_scoops(self, num_scoops): self.num_scoops = num_scoops
    def set_price_per_scoop(self, price): self.price_per_scoop = price
    def set_deluxe_brand(self, deluxe): self.is_deluxe_brand = deluxe
    def set_toppings(self, toppings): self.toppings = toppings
    def get_flavor(self): return self.flavor
    def get_num_scoops(self): return self.num_scoops
    def get_price_per_scoop(self): return self.price_per_scoop
    def get_deluxe_brand(self): return self.is_deluxe_brand
    def get_toppings(self): return self.toppings

    def calc_total(self):
        total = self.num_scoops * self.price_per_scoop
        if self.is_deluxe_brand: total *= 1.42
        for t in self.toppings: total += t.get_cost()
        return total

    def ice_cream_info(self):
        info = f"\nFlavor: {self.flavor}\nScoops: {self.num_scoops}\nDeluxe: {self.is_deluxe_brand}\nToppings: "
        if self.toppings: info += " ".join([t.get_type() for t in self.toppings])
        else: info += "NONE"
        info += f"\nTotal: ${self.calc_total():.2f}\n"
        return info

# ----------------- Receipt Class -----------------
class Receipt:
    def __init__(self):
        self.name = ""
        self.ice_creams = []

    def set_name(self, name): self.name = name
    def add(self, ic): self.ice_creams.append(ic)
    def calc_total(self):
        return sum(i.calc_total() for i in self.ice_creams)
    def print_receipt(self):
        print("\nAdkins' Scoop City Receipt")
        print(f"Customer Name: {self.name}")
        for i in self.ice_creams: print(i.ice_cream_info())
        print(f"Final Total: ${self.calc_total():.2f}")

# ----------------- Main -----------------
def main():
    initialize_db()
    receipt = Receipt()
    order_number = get_next_order_number()
    print("Welcome to Adkins' Scoop City!")
    customer_name = input("What is your name? ")
    receipt.set_name(customer_name)
    still_ordering = True

    while still_ordering:
        ice_cream = IceCream()

        # Flavor
        flavor = input("What flavor of ice cream would you like? ").strip().lower()
        while not ice_cream.validate_flavor(flavor):
            flavor = input("Invalid flavor. Try again: ").strip().lower()
        ice_cream.set_flavor(flavor)

        # Deluxe
        deluxe = input("Would you like the deluxe brand? (Yes/No) ").strip().lower()
        while deluxe not in ["yes", "no"]: deluxe = input("Yes or No only: ").strip().lower()
        ice_cream.set_deluxe_brand(deluxe=="yes")

        # Scoops
        scoops = int(input("How many scoops? "))
        while scoops <= 0: scoops = int(input("Must be >0: "))
        ice_cream.set_num_scoops(scoops)

        # Toppings
        print("Enter toppings (done to finish): sprinkles, gummy bears, oreos, caramel, chocolate chips, peanuts")
        while True:
            topping_type = input().strip().lower()
            if topping_type == "done": break
            topping = Topping()
            if topping.validate_topping(topping_type):
                topping.set_type(topping_type)
                ice_cream.toppings.append(topping)
                print(f"Added {topping.get_type()} for ${topping.get_cost():.2f}")
            else:
                print("Invalid topping")

        receipt.add(ice_cream)

        # Save
        toppings_list = [t.get_type() for t in ice_cream.get_toppings()]
        save_order(order_number, receipt.name, ice_cream.get_flavor(), ice_cream.get_num_scoops(),
                   ice_cream.get_deluxe_brand(), toppings_list, ice_cream.calc_total())

        print("Current order:")
        receipt.print_receipt()

        still = input("Order another? (Yes/No) ").strip().lower()
        while still not in ["yes", "no"]: still = input("Yes or No only: ").strip().lower()
        if still == "no": still_ordering = False; receipt.print_receipt()

if __name__ == "__main__":
    main()