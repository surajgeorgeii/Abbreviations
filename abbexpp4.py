from pathlib import Path

# Defining letters and scores
def get_letter_score(letter, position, is_first, is_last):
    letter_scores = {
        'Q': 1, 'Z': 1, 'J': 3, 'X': 3, 'K': 6,
        'F': 7, 'H': 7, 'V': 7, 'W': 7, 'Y': 7,
        'B': 8, 'C': 8, 'M': 8, 'P': 8,
        'D': 9, 'G': 9,
        'L': 15, 'N': 15, 'R': 15, 'S': 15, 'T': 15,
        'O': 20, 'U': 20,
        'A': 25, 'I': 25,
        'E': 35
    }

    if is_first:
        return 0  # First letter score is 0
    elif is_last:
        return 20 if letter == 'E' else 5  # 'E' gets 20 if last, otherwise 5
    else:
        position_value = 1 if position == 2 else (2 if position == 3 else 3)
        return position_value + letter_scores.get(letter, 0)

def clean_name(name):
    """Cleans non-alphabetic characters and converts to uppercase."""
    return ''.join(char for char in name if char.isalpha() or char.isspace()).upper()

def generate_abbreviations(names):
    """Generates unique three-letter abbreviations with scores."""
    abbreviations = {}

    for name in names:
        clean_name_str = clean_name(name)
        words = clean_name_str.split()

        for word in words:
            for i in range(len(word) - 2):
                abbreviation = word[i] + word[i+1] + word[i+2]
                second_letter, third_letter = word[i+1], word[i+2]
                is_first, is_last = (i == 0), (i + 2 == len(word) - 1)

                score = (get_letter_score(second_letter, 2, is_first, is_last) + 
                         get_letter_score(third_letter, 3, is_first, is_last))

                if abbreviation not in abbreviations:
                    abbreviations[abbreviation] = {'name': name.strip(), 'score': score}
                elif name.strip() != abbreviations[abbreviation]['name']:
                    del abbreviations[abbreviation]
                    break

    return abbreviations

def get_best_abbreviations(abbreviations):
    """Returns a dictionary with the best (lowest-score) abbreviation(s) for each name."""
    best_abbreviations = {}
    for abbreviation, info in abbreviations.items():
        name = info['name']
        score = info['score']
        
        # If the name is not yet in the dictionary or this score is lower, update
        if name not in best_abbreviations or score < best_abbreviations[name]['score']:
            best_abbreviations[name] = {'score': score, 'abbreviations': [abbreviation]}
        # If the score is equal to the best score, add the abbreviation
        elif score == best_abbreviations[name]['score']:
            best_abbreviations[name]['abbreviations'].append(abbreviation)
    
    return best_abbreviations

def write_abbreviations_to_file(best_abbreviations, output_path):
    """Writes best abbreviations and scores to the specified output file."""
    with open(output_path, 'w') as output_file:
        for name, info in best_abbreviations.items():
            abbreviations_line = ' '.join(info['abbreviations'])
            output_file.write(f"{name}\n{abbreviations_line}\n")

def main():
    # Define your surname here for the output file format
    surname = "Kurupassery_George"
    
    # Input file path
    input_file_name = r"C:\Users\HP\OneDrive\Desktop\PYTHON ASSIGNMENT ABBREVATION\trees.txt"
    input_path = Path(input_file_name)
    
    try:
        # Read the input file and process its contents
        with open(input_path, 'r') as file:
            names = file.readlines()
            abbreviations = generate_abbreviations(names)
            best_abbreviations = get_best_abbreviations(abbreviations)

            # Output path following the required format
            output_path = input_path.parent / f"{surname}_{input_path.stem}_abbrevs.txt"
            write_abbreviations_to_file(best_abbreviations, output_path)
            print(f"Abbreviations have been saved to {output_path}")
    except FileNotFoundError:
        print(f"File '{input_file_name}' not found in the specified directory.")

if __name__ == "__main__":
    main()
