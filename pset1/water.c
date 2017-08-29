#include <cs50.h>
#include <stdio.h>


int main(void) 
{
    printf("Minutes: ");
    int n = get_int();
    printf("Bottles: %i\n", n * 12);
}