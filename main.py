#Mariano Ramirez 1963132


import csv
from datetime import datetime

# Read data from CSV files
def read_csv(filename):
    with open(filename, mode='r', newline='') as file:
        reader = csv.reader(file)
        return {rows[0]: rows[1:] for rows in reader}

# Write data to CSV files, allowing for custom sorting and filtering
def write_csv(filename, data, header, sort_key=None, reverse=False):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        if header:
            writer.writerow(header)
        writer.writerows(sorted(data, key=sort_key, reverse=reverse))

# Process full inventory
def process_full_inventory(items, prices, dates):
    full_inventory = []
    for item_id in sorted(items.keys(), key=lambda x: items[x][0]):  # Sort by manufacturer
        full_inventory.append([
            item_id, items[item_id][0], items[item_id][1], prices[item_id][0],
            dates[item_id][0], 'Damaged' if len(items[item_id]) > 2 else ''])
    write_csv('FullInventory.csv', full_inventory, ["Item ID", "Manufacturer", "Item Type", "Price", "Service Date", "Damaged"])

# Process inventory by item type
def process_item_type_inventories(items, prices, dates):
    type_dict = {}
    for item_id, details in items.items():
        item_type = details[1]
        if item_type not in type_dict:
            type_dict[item_type] = []
        type_dict[item_type].append([
            item_id, details[0], prices[item_id][0], dates[item_id][0], 'Damaged' if len(details) > 2 else ''])

    for item_type, data in type_dict.items():
        write_csv(f'{item_type}Inventory.csv', data, ["Item ID", "Manufacturer", "Price", "Service Date", "Damaged"], sort_key=lambda x: x[0])

# Process past service date inventory
def process_past_service_date_inventory(items, prices, dates):
    past_service = []
    today = datetime.now().date()
    for item_id, date in dates.items():
        service_date = datetime.strptime(date[0], '%m/%d/%Y').date()
        if service_date < today:
            past_service.append([
                item_id, items[item_id][0], items[item_id][1], prices[item_id][0], date[0], 'Damaged' if len(items[item_id]) > 2 else ''])
    write_csv('PastServiceDateInventory.csv', past_service, ["Item ID", "Manufacturer", "Item Type", "Price", "Service Date", "Damaged"], sort_key=lambda x: datetime.strptime(x[4], '%m/%d/%Y'))

# Process damaged inventory
def process_damaged_inventory(items, prices):
    damaged = [[item_id, items[item_id][0], items[item_id][1], prices[item_id][0], items[item_id][2]] for item_id in items if len(items[item_id]) > 2]
    write_csv('DamagedInventory.csv', damaged, ["Item ID", "Manufacturer", "Item Type", "Price", "Damaged"], sort_key=lambda x: float(x[3]), reverse=True)

def main():
    # Load data from CSVs
    items = read_csv('ManufacturerList.csv')
    prices = read_csv('PriceList.csv')
    service_dates = read_csv('ServiceDatesList.csv')
    
    # Process data
    process_full_inventory(items, prices, service_dates)
    process_item_type_inventories(items, prices, service_dates)
    process_past_service_date_inventory(items, prices, service_dates)
    process_damaged_inventory(items, prices)

if __name__ == "__main__":
    main()

