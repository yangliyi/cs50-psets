import sys
import cs50

upper_base = 65
lower_base = 97
count_of_letter = 26

if len(sys.argv) != 2:
    print("You should give exactly 2 inputs")
    exit(1)
    
shift_number =int(sys.argv[1])
print("plaintext:  ", end="")
text_input = cs50.get_string()
text_len = len(text_input)

ciphertext = ""
for i in range(text_len):
    char_asc = ord(text_input[i])
    if(char_asc >= upper_base and char_asc <= upper_base + count_of_letter - 1):
        shift = (char_asc + shift_number - upper_base) % count_of_letter
        ciphertext += chr(upper_base + shift)
    elif(char_asc >= lower_base and char_asc <= lower_base + count_of_letter - 1):
        shift = (char_asc + shift_number - lower_base) % count_of_letter
        ciphertext += chr(lower_base + shift)
    else:
        ciphertext += text_input[i]

print("ciphertext: {}".format(ciphertext))