#include <cs50.h>
#include <stdio.h>


int main(void) 
{
    int height;
    printf("Height: ");
    height = get_int();
    while(height < 0 || height > 23)
    {
        printf("Height: ");
        height= get_int();
    }
    
    for (int i = 0; i < height; i++)
    {
        int sum = height + 1;
        int number_of_hash = 2 + i;
        for  (int j = 0; j < sum - number_of_hash; j++)
        {
            printf(" ");
        }
        for  (int k = 0; k < number_of_hash; k++)
        {
            printf("#");
        }
        printf("\n");
    }
}