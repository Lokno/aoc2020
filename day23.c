#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct llnode
{
    struct llnode* n;
    int v;
}llnode;

typedef struct llist
{
    llnode* head;
    llnode* tail;
    llnode* mem;
    unsigned long long size;
    unsigned long long cap;
    int own_mem;
}llist;

llist* init(llnode* mem, unsigned long long cap)
{
    llist* tmp = (llist*)malloc(sizeof(llist));
    tmp->head = NULL;
    tmp->tail = NULL;
    tmp->mem = mem;
    tmp->size = 0u;
    tmp->cap = cap;
    tmp->own_mem = 0;

    if( mem == NULL )
    {
        tmp->mem = (llnode*)calloc(cap,sizeof(llnode));
        tmp->own_mem = 1;
    }

    return tmp;
}

llnode* push( llist* list, int val )
{
    llnode* node = NULL;

    if( val <= 0 ) val = 1;
    if( (unsigned long long)(val-1) < list->cap && list->mem[val-1].v == 0 )
    {
        node = list->mem + (val-1u);

        node->v = val;
        node->n = NULL;
        if( list->head == NULL )
        {
            list->head = node;
            list->tail = list->head;
            list->size = 1u;
        }
        else
        {
            list->tail->n = node;
            list->tail = node;
            list->size++;
        }
    }

    return node;
}

llnode* remove_front3( llist* list )
{
    llnode* tmp = NULL;
    if( list && list->size > 3u )
    {
        tmp = list->head;
        list->head = list->head->n->n->n;
        tmp->n->n->n = NULL;
        list->size -= 3u;  
    }

    return tmp;
}

llnode* roll_lft(llist* list)
{
    llnode* tmp;

    if( list && list->size > 2u )
    {
        tmp = list->head;
        list->head = list->head->n;
        list->tail->n = tmp;
        list->tail = tmp;
        tmp->n = NULL;
    }
}

int max_val(llist* list)
{
    int m = 0;
    llnode* tmp = list->head;

    while( tmp != NULL )
    {
        if( tmp->v > m ) m = tmp->v;
        tmp = tmp->n;
    }
    return m;
}

int insert_at_node(llist* list, llnode* node, llnode* chain)
{
    llnode* ctail = chain;
    while( ctail->n != NULL ) ctail=ctail->n;

    if( node != NULL )
    {
        ctail->n=node->n;
        node->n=chain;
        list->size += 3u;

        if( list->tail == node )
        {
            list->tail = ctail;
        }

        return 1;
    }
    return 0;
}

void delete(llist** list)
{ 
    if( (*list)->own_mem ) free((*list)->mem);
    free(*list);
}

void print_n_from( llist* list, llnode* node, unsigned long long n )
{
    unsigned long long i = 0;
    while( i < n )
    {
        if (node == NULL) node = list->head;
        printf("%d",node->v);
        i++;
        node=node->n;
    }
    printf("\n");
}

void print_chain( llnode* node )
{
    while( node != NULL )
    {
        printf("%d ",node->v);
        node=node->n;
    }
    printf("\n");
}

void move( llist* list, int maxv, llnode* mem )
{
    roll_lft(list);

    llnode* pickup = remove_front3(list);

    int dst = (list->tail->v + (maxv - 2)) % (maxv) + 1;
    while( pickup->v == dst || pickup->n->v == dst || pickup->n->n->v == dst ) 
    {
        dst = (dst + (maxv - 2)) % (maxv) + 1;
    }

    insert_at_node(list,mem+dst-1,pickup);
}

#define NUM_CUPS 1000000

llnode direct[NUM_CUPS];

int main(int argc, char** argv)
{
    llist* list = NULL;
    llnode* tmp = NULL;

    if( argc != 3 )
    {
        printf("Solution to Advent of Code 2020 Day 23\n");
        printf("  usage %s <sequence> <part>\n", argv[0]);
        exit(-1);
    }

    int part = atoi(argv[2]);
    int nums = strlen(argv[1]);
    int count,steps;

    if(part == 1 )
    {
        count = nums;
        steps = 100;
    }
    else
    {
        count = NUM_CUPS;
        steps = 10000000;
    }

    list = init(direct,NUM_CUPS);

    for( int i = 0; i < nums; ++i )
    {
        int input = argv[1][i]-48;
        push(list,input);
    }

    llnode* one = list->mem;

    if( one->v == 0u )
    {
        printf("ERR: The value '1' must appear in the input string\n");
        delete(&list);
        return 0;
    } 

    int maxv = max_val(list);

    int i = maxv;
    while (i++ < count) push(list,i);

    maxv = count;

    while( steps-- > 0 ) move(list,maxv,list->mem);

    if( part == 1 ) print_n_from(list,one->n,8);
    else printf("%lld\n", (long long)one->n->v * (long long)one->n->n->v );

    delete(&list);
    
    return 0;
}