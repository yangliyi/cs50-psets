/**
 * Recover jpeg raw data.
 */
       
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <stdint.h>

typedef uint8_t  BYTE;

int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 2)
    {
        fprintf(stderr, "Usage: ./recover infile \n");
        return 1;
    }

    char *infile = argv[1];

    // open raw data file 
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 2;
    }
    
    int tracker = 0;
    while (true)
    {
        BYTE buffer[512];
        int buffer_size = fread(&buffer, 1, sizeof(buffer), inptr);
        if (buffer_size != 512)
        {
            fclose(inptr);
            return 0;
        }
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            // open new jpeg file
            char filename[8];
            sprintf(filename, "%03i.jpg", tracker);
            FILE *img = fopen(filename, "w");
            if (img == NULL)
            {
                fclose(img);
                fprintf(stderr, "Could not create %s.\n", filename);
                return 3;
            }
            fwrite(&buffer, 1, 512, img);
            
            while (true)
            {
                int size_of_blocks = fread(&buffer, 1, 512, inptr);
                if (size_of_blocks != 512)
                {
                    fclose(img);
                    tracker++;
                    fclose(inptr);
                    return 0;
                }
                else if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
                {
                    fclose(img);
                    tracker++;
                    fseek(inptr, -size_of_blocks, SEEK_CUR);
                    break;
                }
                else
                {
                    fwrite(&buffer, 1, 512, img);
                }
            }
            
        }
    }

    // close infile
    fclose(inptr);

    // success
    return 0;
}

