#include <stdio.h>

#define STB_DS_IMPLEMENTATION
#include "stb_ds.h"

typedef struct sdata
{
    int key;
    int value;
}sdata;

int main(int argc, char** argv)
{
    if( argc < 3 )
    {
        printf("%s <sequence> <turn count>\n", argv[0]);
        exit(-1);
    }

    sdata* lh = NULL;
    int n = atoi(argv[2]);

    int turn = 1;
    int last = -1;

    hmdefault(lh,-1);

    char* pch = strtok(argv[1],",");

    while(pch != NULL)
    {
        int num = atoi(pch);
        hmput(lh,num,turn);
        last = num;
        turn += 1;

        pch = strtok(NULL, ",");
    }

    while(turn <= n)
    {
        int hval = hmget(lh,last);

        if( hval != -1)
        {
            int new = turn-1-hval;
            hmput(lh,last,turn-1);
            last = new;
        }
        else
        {
            hmput(lh,last,turn-1);
            last = 0;          
        }

        turn += 1;
    }

    printf("%d\n",last);

    printf("%ld\n",hmlen(lh));

    hmfree(lh);

    return 0;
}