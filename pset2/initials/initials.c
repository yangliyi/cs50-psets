#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

int main(void) 
{
    string name = get_string();
    int length = strlen(name);
    for(int i = 0; i < length; i++)
    {
        if(i == 0 || name[i-1] == 32)
        {
            printf("%c", toupper(name[i]));
        }
    }
    printf("\n");
}