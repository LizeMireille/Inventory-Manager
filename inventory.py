# This program manages a shoe inventory
# It allows the user to add new shoes to the inventory, view all the shoes, 
# restock the shoe with the lowest quantity, search for a shoe by code, calculate the total value per shoe,
# and view the shoe with the highest quantity in the inventory.

#-----IMPORTS-----
from tabulate import tabulate


#-----CLASS-----
class Shoe:
    def __init__(self, country, code, product, cost, quantity):
        self.country = country
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = quantity

    def get_cost(self):
        return self.cost

    def get_quantity(self):
        return self.quantity

    def __str__(self):
        return f"{self.country}\t{self.code}\t{self.product}\t{self.cost}\t{self.quantity}"

# empty list for holding shoe objects
shoe_list = []


#-----FUNCTIONS-----
def read_shoes_data():
    try:
        with open('inventory.txt', 'r') as file:
# skip the first line (header) and read the remaining lines
            next(file)                              
            for line in file:
# look at each line to create a Shoe object and append it to the shoe list
                data = line.strip().split(',')
                shoes = Shoe(data[0], data[1], data[2], float(data[3]), float(data[4]))   #please see bottom of code for comment on casting choice 
                shoe_list.append(shoes)
    except FileNotFoundError:
        print("Error: inventory file not found")

def capture_shoes():
    print("Please provide the neccessary information on the new shoe:")
    country = input("Country: \n")
    code = input("Code: \n")
    product = input("Product/ Shoe name: \n")
    cost = float(input("Cost: \n"))
    quantity = float(input("Quantity: \n"))
# Create a new Shoe object and add it to the shoe list
    new_shoes = Shoe(country, code, product, cost, quantity)                
    shoe_list.append(new_shoes)
# Add the new_shoes to the inventory file
    with open("inventory.txt", "a") as file:
        file.write(f"\n{country},{code},{product},{cost},{quantity}")
    print("Shoe added successfully")

def view_all():
    headers = ['Country', 'Code', 'Product', 'Cost', 'Quantity']
    rows = []
    for shoe in shoe_list:
# Add each shoe as a row in the table
        rows.append([shoe.country, shoe.code, shoe.product, shoe.cost, shoe.quantity])
    print(tabulate(rows, headers=headers))

def re_stock():
# Find the shoe with the lowest quantity 
    lowest_quantity = shoe_list[0].quantity
    shoe_to_restock = shoe_list[0]
# Loop through the shoes in the shoe_list starting from index 1
    for shoe in shoe_list[1:]:
# If the current shoe has a lower quantity than the previously found shoe with the lowest quantity
        if shoe.quantity < lowest_quantity:
            lowest_quantity = shoe.quantity
            shoe_to_restock = shoe

    print(f"""The shoe with the current lowest quantity in inventory is:
Code:           {shoe_to_restock.code}
Quantity:       {shoe_to_restock.quantity}""")

    add_quantity = input("Do you want to add quantity for this shoe? ('Yes' or 'No') ")
    if add_quantity.lower() == 'yes':
        quantity = float(input("Enter the quantity to be added: "))
# Add the quantity to the selected shoe
        shoe_to_restock.quantity += quantity

# Update the inventory.txt file
        with open("inventory.txt", "r") as file:
            lines = file.readlines()

        with open("inventory.txt", "w") as file:
            for line in lines:
                line_data = line.strip().split(",")
                if line_data[1] == shoe_to_restock.code:
                    line_data[4] = str(shoe_to_restock.quantity)
                    line = ",".join(line_data)
                    file.write(line + "\n")
                else:
                    file.write(line)

        print("Quantity successfully updated")
    elif add_quantity.lower() == 'no':
        print("Quantity not updated")
    else:
        print("You have entered an invalid response.")


def search_shoe():
    code = input("Enter the code of the shoe: ")
    for shoe in shoe_list:
        if shoe.code == code:
            print(shoe)
# Exit the function
            return
# If the code input by the user doesn't match any of the shoes in the shoe_list
    print("Shoe not found")

def value_per_item():
# Create headers for the table 
    headers = ["Product", "Value"]
# Create an empty list to store the rows of data for each shoe
    rows = []
# Loop through each shoe in shoe_list
    for shoe in shoe_list:
        value = shoe.cost * shoe.quantity
        rows.append([shoe.product, value])
    print(tabulate(rows, headers=headers))


def highest_qty():
    # Set initial value for the highest quantity to the quantity of first shoe in list
    highest_quantity = shoe_list[0].quantity
    # Set initial shoe for sale to be the first shoe in list
    shoe_for_sale = shoe_list[0]
    
    for shoe in shoe_list:
        if shoe.quantity > highest_quantity:
            highest_quantity = shoe.quantity
            shoe_for_sale = shoe
    
    print(f"""The shoe with the current highest quantity in inventory is:
Product:        {shoe_for_sale.product}
Code:           {shoe_for_sale.code}
Quantity:       {shoe_for_sale.quantity}""")

    return shoe_for_sale

#-----USER SELECTION-----

# Read in the data from inventory.txt
read_shoes_data()

# Loop through the menu options until the user chooses to exit
while True:
    menu = input('''Please select one of the following options:
c   - capture shoe
va  - view all shoes 
r   - restock the lowest quantity shoe
s   - search a shoe by code
v   - calculate the total value per shoe
hq  - view the shoe with the current higest quantity
e   - exit\n''').lower()

    if menu == "c":
        capture_shoes()
    
    elif menu == "va":
        view_all()
    
    elif menu== "r":
        re_stock()
    
    elif menu == "s":
        search_shoe()
    
    elif menu == "v":
        value_per_item()
    
    elif menu == "hq":
        highest_qty()
    
    elif menu == "e":
        print('Goodbye!!!')
        exit()

    else:
        print("You have made an invalid selection. Please Try again!")
