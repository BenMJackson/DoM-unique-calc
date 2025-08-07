def get_completions_input():
    completions = {}
    print("Enter number of completions for each floor (leave blank for 0):")
    for floor in range(2, 10):
        try:
            val = input(f"  Floor {floor}: ").strip()
            completions[floor] = int(val) if val else 0
        except ValueError:
            print("Invalid input. Assuming 0.")
            completions[floor] = 0
    return completions


def calculate_no_drop_chance(rate, kills):
    return (1 - 1 / rate) ** kills


def calculate_overall_unique_chance(completions):
    cumulative_drop_rates = {
        2: 2500,
        3: 1111,
        4: 610,
        5: 348,
        6: 239,
        7: 179,
        8: 140,
        9: 111,
    }

    p_no_unique = 1.0
    for floor, kills in completions.items():
        if floor in cumulative_drop_rates and kills > 0:
            rate = cumulative_drop_rates[floor]
            p_no_unique *= calculate_no_drop_chance(rate, kills)

    return 1 - p_no_unique


def calculate_item_chance(completions, item_floors):
    p_no_item = 1.0
    for floor, rate in item_floors.items():
        if completions.get(floor, 0) > 0:
            p_no_item *= calculate_no_drop_chance(rate, completions[floor])
    return 1 - p_no_item


def main():
    completions = get_completions_input()

    # 1. Overall unique drop chance
    overall_chance = calculate_overall_unique_chance(completions)
    print(f"\n💠 Overall chance of at least one unique: {overall_chance * 100:.2f}%")

    # 2. Individual item chances
    unique_items = {
        "Mokhaiotl Cloth": {
            3: 2000,
            4: 1350,
            5: 810,
            6: 765,
            7: 720,
            8: 630,
            9: 540,
        },
        "Eye of Ayak": {
            4: 1350,
            5: 810,
            6: 765,
            7: 720,
            8: 630,
            9: 540,
        },
        "Avernic Treads": {
            6: 1000,
            7: 750,
            8: 500,
            9: 250,
        },
        "Dom": {
            7: 429,
            8: 231,
            9: 120,
        },
    }

    print("\n📦 Individual unique drop chances:")
    for item, item_floors in unique_items.items():
        chance = calculate_item_chance(completions, item_floors)
        print(f"  {item}: {chance * 100:.2f}%")

if __name__ == "__main__":
    main()