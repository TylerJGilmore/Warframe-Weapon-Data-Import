import csv
import requests

# GET weapon data 
def fetch_all_weapons():
    url = "https://api.warframestat.us/weapons"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to fetch weapon data.")
        return None

def fetch_weapon_stats(weapon_name):
    url = f"https://api.warframestat.us/weapons/{weapon_name}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch weapon stats: {url}")
        return None

def export_to_csv(weapons):
    fieldnames = ['Weapon', 'Stat', 'Value']

    with open('weapon_stats.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for weapon in weapons:
            weapon_name = weapon['name']
            weapon_stats = fetch_weapon_stats(weapon_name)
            if weapon_stats is not None:
                for stat_name, stat_value in weapon_stats.items():
                    if stat_name != 'name':
                        writer.writerow({'Weapon': weapon_name, 'Stat': stat_name, 'Value': stat_value})

    print("Export to CSV complete. The data has been saved to 'weapon_stats.csv'.")

def extract_substat_types(weapons):
    substat_types = set()

    for weapon in weapons:
        weapon_name = weapon['name']
        weapon_stats = fetch_weapon_stats(weapon_name)
        if weapon_stats is not None:
            for stat_name in weapon_stats.keys():
                if stat_name != 'name':
                    substat_types.add(stat_name)

    return substat_types

def save_substat_types(substat_types):
    with open('substat_types.txt', 'w') as file:
        for substat_type in substat_types:
            file.write(substat_type + '\n')

    print("Substat types saved to 'substat_types.txt'.")

def main():
    weapon_data = fetch_all_weapons() # GET request to server. NOT 200 = Failed to GET
    if weapon_data is None:
        return

    # Determine total number of weapons returned
    weapons = weapon_data
    total_weapons = len(weapons)
    print(f"Total weapons found: {total_weapons}\n")

    progress_counter = 0 # Counting weapons completed out of the total grabbed

    # Progress display
    for weapon in weapons:
        progress_counter += 1
        print(f"Processing weapon {progress_counter}/{total_weapons}...")
        
        # Displays GET return
        weapon_name = weapon['name']
        weapon_stats = fetch_weapon_stats(weapon_name)
        if weapon_stats is not None:
            for stat_name, stat_value in weapon_stats.items():
                if stat_name != 'name':
                    print(f"{stat_name}: {stat_value}")

        print()  # Newline for cleanliness

    export_to_csv(weapons)
    substat_types = extract_substat_types(weapons)
    save_substat_types(substat_types)

if __name__ == "__main__":
    main()
