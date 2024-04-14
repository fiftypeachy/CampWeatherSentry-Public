from fuzzywuzzy import process

from list_of_camp_names import camps


def search_camps(query):
    # return [name for name in camps if query.lower() in name.lower()]
    matches = process.extract(query, camps)

    return [camp[0] for camp in matches if camp[1] > 70]


def handle_user_input():
    while True:
        query = input("    Enter search query: ")
        results = search_camps(query)
        if len(results) == 1:
            return results[0]
        print("Closest results:")
        counter = 1
        for result in results:
            print(f"{counter}:", result)
            counter += 1

        while True:
            try:
                num = int(input("Choose a camp or enter 0 to re-enter a new query: "))
            except ValueError:
                print("Invalid input.")
                continue

            if num < 0 or num > counter:
                print("Invalid input.")
                continue

            elif num == 0:
                break

            else:
                return results[num - 1]
