/**
 * Implements a dictionary's functionality.
 */

#include <ctype.h>

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "dictionary.h"
#define NUMBER_OF_CHARACTER 26

unsigned int number_of_words = 0;     // global var to save number of words

typedef struct node
{
    bool end_of_word;
    struct node *children[NUMBER_OF_CHARACTER+1];
} node;

node root = {false,{NULL}};

int charPosition(char c)
{
    int num;
    if (c == '\'')
        return 26;

    num = c - 'a';
    return num;
}

/**
 * Loads dictionary into memory. Returns true if successful else false.
 */
bool load(const char *dictionary)
{

    FILE *fp = fopen(dictionary, "r");
    if (fp == NULL)
    {
        printf("Could not open %s.\n", dictionary);
        return false;
    }

    // load the whole dic file until the end of file
    node *ptr = &root;
    for (int c = fgetc(fp); c != EOF; c = fgetc(fp))
    {
        if (c == '\n')
        {
            // Should have at least one letter
            if (ptr != &root)
            {
                number_of_words++;
                ptr->end_of_word = true;

                ptr = &root;        
            }
        }
        else
        {
            char lower_c = tolower(c);
            int cp = charPosition(lower_c);

            if (ptr->children[cp] == NULL)
            {
                node *nextNode = malloc(sizeof(node));
                *nextNode = (node) { false, { NULL } };
                ptr->children[cp] = nextNode;
                ptr = nextNode;
            }
            else
            {
                ptr = ptr->children[cp];
            }
            
        }
    }

    fclose(fp);
    return true;
}

/**
 * Returns true if word is in dictionary else false.
 */
bool check(const char *word)
{
    int length = strlen(word);
    node *ptr = &root;

    for( int i = 0; i < length; i++)
    {
        char c = tolower(word[i]);
        int cp = charPosition(c);
        node* nextNode = ptr->children[cp];
        if (nextNode == NULL)
        {
            return false;
        }
        else
        {
            ptr = nextNode;
        }
    }
    if (ptr->end_of_word == true)
    {
        return true;
    }
    
    return false;
}
/**
 * Returns number of words in dictionary if loaded else 0 if not yet loaded.
 */
unsigned int size(void)
{
    if (number_of_words) 
    {
        return number_of_words;
    }
    return 0;
}

void freeNode(node *currentNode)
{
    for (int i = 0; i < NUMBER_OF_CHARACTER + 1; i++)
    {
        if (currentNode->children[i] != NULL)
            freeNode(currentNode->children[i]);
    }
    free(currentNode);
}

/**
 * Unloads dictionary from memory. Returns true if successful else false.
 */
bool unload(void)
{
    for (int i = 0; i < NUMBER_OF_CHARACTER + 1; i++)            
    {
        if (root.children[i] != NULL) 
            freeNode(root.children[i]);
    }
    return true;
}