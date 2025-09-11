"""
Author:         Jake Bredice
Date:           11-4
Assignment:     Lab 08
Course:         CPSC1051
Lab Section:    SECTION 101

CODE DESCRIPTION:
Icecream ordering system

"""
# Topping class that has the attributes of type and cost.
class Topping:
    def __init__(self):
        """Initializes the topping's type and cost."""
        self.type = ""
        self.cost = 0.0

    def validate_topping(self, type):
        """Confirms that the toppings are a valid choice"""
        return type.lower() in ["sprinkles", "gummy bears", "oreos", "done"]

    def set_type(self, type):
        """Sets the type of the topping and the cost of the topping."""
        self.type = type.lower()
        if self.type == "sprinkles":
            self.cost = 0.15
        elif self.type == "gummy bears":
            self.cost = 0.45
        elif self.type == "oreos":
            self.cost = 0.38

    def get_type(self):
        """Returns the type of the topping."""
        return self.type

    def get_cost(self):
        """Returns the cost of the topping."""
        return self.cost

# Represent the IceCream that has the following attributes:
# Flavor, number of scoops, price per scoop, if deluxe or not, list of toppings
class IceCream:
    def __init__(self):
        """Initializes the IceCream class with its default values."""
        self.flavor = ""
        self.num_scoops = 0
        self.price_per_scoop = 0.0
        self.is_deluxe_brand = False
        self.toppings = []

    def validate_flavor(self, flavor):
        """Returns true or false depending on if the flavor exists."""
        return flavor.lower() in ["vanilla", "chocolate", "strawberry"]

    def set_flavor(self, flavor):
        """Sets the flavor and price of the flavor"""
        self.flavor = flavor.lower()

        if self.flavor == "vanilla":
            self.price_per_scoop = 1.05
        elif self.flavor == "chocolate":
            self.price_per_scoop = 1.12
        elif self.flavor == "strawberry":
            self.price_per_scoop = 1.32

    def get_flavor(self):
        """Returns the flavor of the IceCream."""
        return self.flavor

    def set_num_scoops(self, num_scoops):
        """Sets the number of scoops the IceCream has."""
        self.num_scoops = num_scoops

    def get_num_scoops(self):
        """Returns the number of scoops the IceCream has."""
        return self.num_scoops

    def set_price_per_scoop(self, price_per_scoop):
        """Sets the price per scoop of the IceCream."""
        self.price_per_scoop = price_per_scoop

    def get_price_per_scoop(self):
        """Returns the price per scoop of IceCream."""
        return self.price_per_scoop

    def set_deluxe_brand(self, deluxe):
        """Sets whether or not the IceCream is deluxe"""
        self.is_deluxe_brand = deluxe

    def get_deluxe_brand(self):
        """Returns true if the IceCream is deluxe, false otherwise."""
        return self.is_deluxe_brand

    def set_toppings(self, toppings):
        """Sets the list of toppings the IceCream has."""
        self.toppings = toppings

    def get_toppings(self):
        """Returns the list of toppings the IceCream has."""
        return self.toppings

    def calc_total(self):
        """ Returns the total of the current IceCream."""
        total = self.num_scoops * self.price_per_scoop
        if self.is_deluxe_brand:
            total *= 1.42
        for t in self.toppings:
            total += t.get_cost()
        return total

    def ice_cream_info(self):
        """Returns a string representation of the ice cream flavor for the receipt."""
        info = ""
        info += f"\nFlavor: {self.flavor}"
        info += f"\nScoops: {self.num_scoops}"
        info += f"\nDeluxe: {self.is_deluxe_brand}"
        info += "\nToppings: "
        for t in self.toppings:
            info += t.get_type() + " "
        if not self.toppings:
            info += "NONE"
        info += f"\nTotal: ${self.calc_total():.2f}\n"
        return info

# Represents the Receipt which has the following attributes:
# name of the customer and list of ice creams.
class Receipt:
    def __init__(self):
        """Initializes the receipt class's name and list of ice creams."""
        self.name = ""
        self.ice_creams = []

    def set_name(self, name):
        """Sets the name of the customer on the receipt"""
        self.name = name

    def add(self, ic):
        """Adds an ice cream to the receipt."""
        self.ice_creams.append(ic)

    def calc_total(self):
        """Calculates the total price of all of the ice creams."""
        total = 0
        for i in self.ice_creams:
            total += i.calc_total()
        return total

    def print_receipt(self):
        """Prints out the customer's receipt"""
        print("\nAdkins' Scoop City Receipt")
        print(f"Customer Name: {self.name}")
        for i in self.ice_creams:
            print(i.ice_cream_info())
        print(f"Final Total: ${'{:.2f}'.format(self.calc_total())}")

def main():
    #Welcomes player and stores name in receipt
    receipt = Receipt()
    print("Welcome to Adkins' Scoop City!")
    print("What is your name?")
    customer_name = input()
    receipt.set_name(customer_name)
    still_ordering = True

    while still_ordering:
    # Start of single icecream order loop
        ice_cream = IceCream()

    # Flavor selection, validation, and setting
        print("What flavor of ice cream would you like to order?")
        print("Your options are: Vanilla, Strawberry, Chocolate.")
        flavor = input().strip().lower()
        while not ice_cream.validate_flavor(flavor):
            print("Please put in a valid ice cream flavor.")
            flavor = input().strip().lower()
        ice_cream.set_flavor(flavor)
    # Deluxe selection, validation, and setting
        print("Would you like the deluxe brand? (Yes/No)")
        deluxe = input().strip().lower()
        while deluxe not in ["yes", "no"]:
            print("Please input Yes or No!")
            deluxe = input().strip().lower()
        if deluxe == "yes":
            deluxe = True
            ice_cream.set_deluxe_brand(deluxe)
    # Scoops selection, validation, and setting
        print("How many scoops would you like to order?")
        scoops = int(input())
        while scoops <= 0:
            print("Please enter a number greater than 0")
            scoops = int(input())
        ice_cream.set_num_scoops(scoops)
    # Toppings selection, validation, and setting
        print("Which toppings would you like? Enter done if you do not want any.")
        print("Your options are: sprinkles, gummy bears, oreos.")
        while True:
            topping_type = input().strip().lower()
            if topping_type == "done":
                break
            topping = Topping()
            if topping.validate_topping(topping_type):
                topping.set_type(topping_type)
                ice_cream.toppings.append(topping)
                print(f"Topping {topping.get_type()} added for ${topping.get_cost():.2f}")
                print("Enter done if you are done selecting toppings, or enter another topping.")
            else:
                print("Please put in a valid topping type.")
        receipt.add(ice_cream)
        print("Your order so far:")
        receipt.print_receipt()
    #If user selects yes, they will restart the icecream ordering loop, otherwise it will print the receipt
        print("Would you like to order another ice cream? (Yes/No)")
        still = input().strip().lower()
        while still not in {"yes", "no"}:
            print("Please input Yes or No!")
            still = input().strip().lower()
        if still == "no":
            still_ordering = False   
            receipt.print_receipt()

# Runs main
if __name__ == "__main__":
    main()
