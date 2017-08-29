#include <cs50.h>
#include <stdio.h>
#include <math.h>


int main(void) 
{
    float cents;
    printf("O hai! How much change is owed?\n");
    cents = get_float();
    while(cents < 0)
    {
        printf("O hai! How much change is owed?\n");
        cents = get_float();
    }
    
    float float_dollar = cents * 100;
    float rount_dollar = round(float_dollar);
    int dollar = (int)rount_dollar;
    int number_of_coins = 0;
    while (dollar >= 25)
    {
        dollar -= 25;
        number_of_coins += 1;
    }
    while (dollar >= 10)
    {
        dollar -= 10;
        number_of_coins += 1;
    }
    while (dollar >= 5)
    {
        dollar -= 5;
        number_of_coins += 1;
    }
    printf("%i\n", number_of_coins + dollar);
}