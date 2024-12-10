from collections import Counter
import re

LETTER_VALUES = {
    'A': 25, 'B': 8, 'C': 8, 'D': 9, 'E': 35, 'F': 7,
    'G': 9, 'H': 7, 'I': 25, 'J': 3, 'K': 6, 'L': 15,
    'M': 8, 'N': 15, 'O': 20, 'P': 8, 'Q': 1, 'R': 15,
    'S': 15, 'T': 15, 'U': 20, 'V': 7, 'W': 7, 'X': 3,
    'Y': 7, 'Z': 1
}

def clean_name(name):
    """Cleans and splits the name into words."""
    return [word.upper() for word in re.findall(r'[A-Za-z]+', name)]

def calculate_letter_score(word, letter, position):
    """Calculates the score for a letter based on its position in the word."""
    if position == 0:
        return 0
    elif position == len(word) - 1:
        return 20 if letter == 'E' else 5
    else:
        position_value = 1 if position == 1 else 2 if position == 2 else 3
        return position_value + LETTER_VALUES[letter]

def calculate_abbreviation_score(name, abbreviation):
    """calculates total score of an abbreviation."""
    words = clean_name(name)
    combined = ''.join(words)
    score = 0

    word_starts = []
    current_index = 0
    for word in words:
        word_starts.append(current_index)
        current_index += len(word)

    used_indexes = set()
    for letter in abbreviation[1:]:
        index = next(
            (i for i in range(len(combined)) if combined[i] == letter and i not in used_indexes),
            -1
        )
        if index == -1:
            continue

        for word_index, start_index in enumerate(word_starts):
            if start_index <= index < start_index + len(words[word_index]):
                word = words[word_index]
                position = index - start_index
                letter_score = calculate_letter_score(word, letter, position)
                score += letter_score
                break

        used_indexes.add(index)

    return score

def generate_abbreviations(name):
    """Generates all possible abbreviations for a name."""
    words = clean_name(name)
    combined = ''.join(words)
    abbreviations = []
    first_letter = combined[0]

    for i in range(1, len(combined) - 1):
        for j in range(i + 1, len(combined)):
            abbreviations.append(first_letter + combined[i] + combined[j])
    return abbreviations

def resolve_duplicates(abbreviation_scores):
    """Resolves duplicates and lists all abbreviations with the same best score."""
    global_abbreviation_map = Counter(
        abbr for scores in abbreviation_scores.values() for abbr in scores
    )

    unique_abbreviations = {}
    for name, scores in abbreviation_scores.items():
        # Filter out abbreviations that are shared among multiple names
        valid_abbrs = {
            abbr: score for abbr, score in scores.items() if global_abbreviation_map[abbr] == 1
        }

        # If valid abbreviations exist, find the one with the minimum score
        if valid_abbrs:
            min_score = min(valid_abbrs.values())
            best_abbrs = [abbr for abbr, score in valid_abbrs.items() if score == min_score]
        else:
            # If no unique abbreviation exists, leave blank
            best_abbrs = []

        unique_abbreviations[name] = best_abbrs

    return unique_abbreviations

def main():
    input_file = "trees.txt"  #input file path
    output_file = "trees_abbrevation_output.txt"  # Output file path 

    # Read names from the file
    with open(input_file, 'r') as file:
        names = [line.strip() for line in file if line.strip()]

    abbreviation_scores = {}
    for name in names:
        abbreviations = generate_abbreviations(name)
        scores = {abbr: calculate_abbreviation_score(name, abbr) for abbr in abbreviations}
        abbreviation_scores[name] = scores

    unique_abbreviations = resolve_duplicates(abbreviation_scores)

    # Write results to the output file
    with open(output_file, 'w') as file:
        for name, abbreviations in unique_abbreviations.items():
            abbreviation_line = " ".join(abbreviations) if abbreviations else ""
            file.write(f"{name}\n{abbreviation_line}\n")

    print(f"Abbreviations saved to {output_file}")

if __name__ == "__main__":
    main()

