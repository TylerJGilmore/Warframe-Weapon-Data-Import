import csv
import requests

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

    print("Export complete. The data has been saved to 'weapon_stats.csv'.")

def main():
    weapon_data = fetch_all_weapons()
    if weapon_data is None:
        return

    weapons = weapon_data
    print(f"Total weapons found: {len(weapons)}\n")

    export_to_csv(weapons)

if __name__ == "__main__":
    main()
