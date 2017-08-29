/**
 * helpers.c
 *
 * Helper functions for Problem Set 3.
 */
 
#include <cs50.h>
#include <stdio.h>
#include "helpers.h"


/**
 * Returns true if value is in array of n values, else false.
 */
bool search(int value, int values[], int n)
{
    if (value <= 0) 
    {
        return false;
    }

    int list_size = n;
    int left_index = 0;
    int right_index = n-1;

    while (list_size > 0)
    {
        int middle_index = (left_index + right_index) / 2;
        if (value == values[middle_index])
        {
            return true;
        }
        else if (value > values[middle_index])
        {
            left_index = middle_index+1;
        }
        else {
            right_index = middle_index-1;
        }
        list_size = right_index - left_index + 1;
    }
    return false;
    
}

/**
 * Sorts array of n values.
 */
void sort(int values[], int n)
{
    for(int i = 0; i < n-1; i++)
    {
        for(int i = 0; i < n-1; i++)
        {
            if (values[i] > values [i+1])
            {
                int temp = values[i];
                values[i] = values[i+1];
                values[i+1] = temp;
            }
        }
    }
    
    return;
}
