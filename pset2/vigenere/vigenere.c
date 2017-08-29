#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#define UPPER_BASE 65
#define LOWER_BASE 97
#define COUNT_OF_LETTER 26

int update_position(int position, int length);
int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("You should give exactly 2 inputs\n");
        return 1;
    }
    string shift_code = argv[1];
    int shift_len = strlen(shift_code);
    for (int i = 0; i < shift_len; i++)
    {
        if (toupper(shift_code[i]) < UPPER_BASE || toupper(shift_code[i]) > UPPER_BASE + COUNT_OF_LETTER - 1)
        {
            printf("You should use all English characters as keyword\n");
            return 1;
        }
    }

    printf("plaintext:  ");
    string text_input = get_string();
    int text_len = strlen(text_input);
    
    printf("ciphertext: ");
    int shift_position = 0;
    for(int i = 0; i < text_len; i++)
    {
        if(text_input[i] >= UPPER_BASE && text_input[i] <= UPPER_BASE + COUNT_OF_LETTER - 1)
        {
            int shift = ((toupper(shift_code[shift_position]) - UPPER_BASE)+ text_input[i] - UPPER_BASE) % COUNT_OF_LETTER;
            printf("%c", UPPER_BASE + shift);
            shift_position = update_position(shift_position, shift_len);
        }
        else if(text_input[i] >= LOWER_BASE && text_input[i] <= LOWER_BASE + COUNT_OF_LETTER - 1)
        {
            int shift = ((toupper(shift_code[shift_position]) - UPPER_BASE)+ text_input[i] - LOWER_BASE) % COUNT_OF_LETTER;
            printf("%c", LOWER_BASE + shift);
            shift_position = update_position(shift_position, shift_len);
        }
        else
        {
            printf("%c", text_input[i]);
        }
    }
    printf("\n");
}

int update_position(int position, int length)
{
    if (position + 1 < length)
    {
        return position + 1;
    }
    else
    {
        return 0;
    }
}