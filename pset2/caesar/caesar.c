#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#define UPPER_BASE 65
#define LOWER_BASE 97
#define COUNT_OF_LETTER 26

int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("You should give exactly 2 inputs\n");
        return 1;
    }
    int shift_number = atoi(argv[1]);
    printf("plaintext:  ");
    string text_input = get_string();
    int text_len = strlen(text_input);
    
    printf("ciphertext: ");
    for(int i = 0; i < text_len; i++)
    {
        if(text_input[i] >= UPPER_BASE && text_input[i] <= UPPER_BASE + COUNT_OF_LETTER - 1)
        {
            int shift = (shift_number + text_input[i] - UPPER_BASE) % COUNT_OF_LETTER;
            printf("%c", UPPER_BASE + shift);
        }
        else if(text_input[i] >= LOWER_BASE && text_input[i] <= LOWER_BASE + COUNT_OF_LETTER - 1)
        {
            int shift = (shift_number + text_input[i] - LOWER_BASE) % COUNT_OF_LETTER;
            printf("%c", LOWER_BASE + shift);
        }
        else
        {
            printf("%c", text_input[i]);
        }
    }
    printf("\n");
}
