import sys
import random
import csv

def get_random_choice(lst):
  return random.choice(lst)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: gen_mnm_dataset entries", file=sys.stderr)
        sys.exit(-1)

    states = ["CA", "WA", "TX", "NV", "CO", "OR", "AZ", "WY", "NM", "UT"]
    colors = ["Brown", "Blue", "Orange", "Yellow", "Green", "Red"]
    fieldnames = ['State', 'Color', 'Count']


    try:
        entries = int(sys.argv[1])
        if entries <= 0:
            raise ValueError("Entries must be a positive integer.")
    except ValueError:
        print(f"Error: Invalid argument for entries: '{sys.argv[1]}'. Must be a positive integer.", file=sys.stderr)
        sys.exit(-1)

    dataset_fn = "mnm_dataset.csv"

    with open(dataset_fn, mode='w') as dataset_file:
        dataset_writer = csv.writer(dataset_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        dataset_writer.writerow(fieldnames)
        for i in range(1, entries):
            dataset_writer.writerow([get_random_choice(states), get_random_choice(colors), random.randint(10, 100)])
    print("Wrote %d lines in %s file" % (entries, dataset_fn))
