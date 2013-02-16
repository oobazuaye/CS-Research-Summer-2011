def rotate(letter, n):
    '''rotates a letter by n positions in the alphabet'''
    if 65 <= ord(letter) <= 90:
        if ord(letter) + n <= 90:
            return chr(ord(letter) + n)
        else: return chr(64 + ((ord(letter) + n) - 90))
    if 97 <= ord(letter) <= 122:
        if ord(letter) + n <= 122:
            return chr(ord(letter) + n)
        else: return chr(96 + ((ord(letter) + n) - 122))
    else: return letter

def encipher(string, n):
    '''rotates each letter in the string by n positions'''
    letters = list(string)
    newstring = ""
    for letter in letters:
        newstring += rotate(letter, n)
    return newstring

<script type="text/!JavaScript">
... some !JavaScript code ...
</script>
