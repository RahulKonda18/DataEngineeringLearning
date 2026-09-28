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


    entries = int(sys.argv[1])
    dataset_fn = "mnm_dataset.csv"

    num_rows = max(0, entries - 1)
    chunk_size = 100000
    counts_range = range(10, 101)

    with open(dataset_fn, mode='w') as dataset_file:
        dataset_writer = csv.writer(dataset_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        dataset_writer.writerow(fieldnames)
        remaining = num_rows
        while remaining > 0:
            current_chunk = min(remaining, chunk_size)
            rand_states = random.choices(states, k=current_chunk)
            rand_colors = random.choices(colors, k=current_chunk)
            rand_counts = random.choices(counts_range, k=current_chunk)
            dataset_writer.writerows(zip(rand_states, rand_colors, rand_counts))
            remaining -= current_chunk
    print("Wrote %d lines in %s file" % (entries, dataset_fn))
