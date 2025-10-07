import random
from main import IceCream, Receipt, Topping
import icecream_db
from datetime import datetime, timedelta

# ---------------- Options -----------------
flavors_base = ["vanilla", "chocolate", "strawberry", "mint", "cookies and cream", "rocky road", "coffee"]
toppings_options = ["sprinkles", "gummy bears", "oreos", "caramel", "chocolate chips", "peanuts"]
names = ["Alice", "Bob", "Charlie", "Dana", "Eli", "Fay", "Gus", "Hana", "Ivy", "Jack"]

# ---------------- Helper -----------------
def random_created_at(start_year=2025, months_back=12):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30*months_back)
    random_date = start_date + (end_date - start_date) * random.random()
    return random_date.strftime("%Y-%m-%d %H:%M:%S")

def random_ice_cream(created_at=None):
    ic = IceCream()

    # Month for seasonal flavors
    if created_at:
        month = int(created_at[5:7])
    else:
        month = random.randint(1, 12)

    # Seasonal flavors
    seasonal = []
    if month in [12,1]: seasonal.append("peppermint")
    if month in [9,10,11]: seasonal.append("pumpkin")
    if month in [6,7,8]: seasonal.append("mango")
    if month in [3,4,5]: seasonal.append("strawberry cheesecake")

    all_flavors = flavors_base + seasonal
    ic.set_flavor(random.choice(all_flavors))
    ic.set_num_scoops(random.randint(1,5))
    ic.set_deluxe_brand(random.choice([True, False]))

    num_toppings = random.randint(0,3)
    toppings = random.sample(toppings_options, num_toppings)
    topping_objs = []
    for t in toppings:
        top = Topping()
        top.set_type(t)
        topping_objs.append(top)
    ic.set_toppings(topping_objs)
    return ic

def generate_orders(n_orders=100):
    for _ in range(n_orders):
        receipt = Receipt()
        receipt.set_name(random.choice(names))
        created_at = random_created_at()
        order_number = icecream_db.get_next_order_number()
        num_ice_creams = random.randint(1,3)

        for _ in range(num_ice_creams):
            ic = random_ice_cream(created_at)
            receipt.add(ic)
            toppings_list = [t.get_type() for t in ic.get_toppings()]
            icecream_db.save_order(order_number, receipt.name, ic.get_flavor(),
                                   ic.get_num_scoops(), ic.get_deluxe_brand(),
                                   toppings_list, ic.calc_total(), created_at)

if __name__ == "__main__":
    order_n = int(input("How many orders to generate? "))
    generate_orders(order_n)
    print(f"{order_n} random orders added to database!")