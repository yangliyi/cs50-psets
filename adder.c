#include <cs50.h>
#include <stdio.h>

int main(void)
{
    printf("x is: ");
    int x = get_int();
    printf("y is: ");
    int y = get_int();

    printf("x + y = %i \n", x + y);

}