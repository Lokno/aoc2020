#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int get_keys(const char * filename, size_t* a, size_t*b)
{
    size_t data[2] = {0u,0u};
    size_t ele_num = 0u;
    int succ = 0;
    int keys = 2;
    int i = 0;

    *a = 0u;
    *b = 0u;

    FILE* fptr = fopen(filename, "r");
    char* file_contents = NULL;
    if( fptr != NULL )
    {
        fseek(fptr, 0, SEEK_END);
        long fsize = ftell(fptr);
        fseek(fptr, 0, SEEK_SET);
        file_contents = malloc(fsize + 1);
        if( file_contents != NULL )
        {
            ele_num = fread(file_contents, 1, fsize, fptr);
        }
        fclose(fptr);

        if( fsize != ele_num )
        {
            free(file_contents);
            file_contents = NULL;
        }
    }

    if( file_contents != NULL )
    {
        char* pch = strtok(file_contents,"\n");
        while( i < 2 && pch != NULL)
        {
            data[i++] = (size_t)atol(pch);
            pch = strtok(NULL, "\n");
        }

        if( i == 2 )
        {
            *a = data[0];
            *b = data[1];
            succ = 1;
        }

        free(file_contents);
    }

    return succ;
}

#define transform(x,s) ((x*s) % 20201227u)

int main(int argc, char** argv)
{
    if( argc != 2)
    {
        printf("Solution to Advent of Code 2020 Day 25\n"
               "   usage: %s <filename>\n",argv[0]);
        exit(-1);
    }

    size_t publica;
    size_t publicb;

    if( get_keys(argv[1], &publica, &publicb) )
    {
        size_t val = 1u;
        size_t ekey = 1u;
        while (val != publica) {
            val = transform(val,7u);
            ekey = transform(ekey,publicb);
        }
        printf("%lu\n",ekey);        
    }
    else
    {
        printf("ERROR: failed to read keys\n");
    }

    return 0;
}