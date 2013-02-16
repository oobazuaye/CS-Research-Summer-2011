def syllables(word):
    letters = map(ord, list(word))
    vowels = map(ord, ["a", "e", "i", "o", "u", "y", "A", "E", "I", "O", "U", "Y"])
    syllables = 0
    consonant = 0
    if letters[0] in vowels:
        syllables+=1
    for letter in letters:
        if letter not in vowels:
            consonant = 1
        if consonant == 1 and letter in vowels:
            if letter == letters[-1] and (letter == ord("e") or letter == ord("E")):
                0
            else: syllables+=1
            consonant = 0
        
    return syllables
            
