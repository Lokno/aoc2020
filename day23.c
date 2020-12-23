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
    llnode* third;
    unsigned long long size;
}llist;

llist* init()
{
    llist* tmp = (llist*)malloc(sizeof(llist));
    tmp->head = NULL;
    tmp->tail = NULL;
    tmp->third = NULL;
    tmp->size = 0u;
    return tmp;
}

llnode* push( llist* list, int val )
{
    llnode* node = (llnode*)malloc(sizeof(llnode));
    node->v = val;
    node->n = NULL;
    if( list->head == NULL )
    {
        list->head = node;
        list->tail = list->head;
        list->third = NULL;
        list->size = 1u;
    }
    else
    {
        list->tail->n = node;
        list->tail = node;

        list->size++;

        if( list->size == 3u )
        {
            list->third=node;
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
        list->head = list->third->n;
        list->third->n = NULL;
        list->size -= 3u;

        if( list->size >= 3 )
        {
            list->third=list->head->n->n;
        }
        else
        {
            list->third=NULL;
        }
        
    }

    return tmp;
}

llnode* roll_lftn(llist* list, int n)
{
    llnode* tmp;

    if( list && list->size > 2u )
    {
        for(int i = 0; i < n; ++i)
        {
            tmp = list->head;
            list->head = list->head->n;
            list->tail->n=tmp;
            list->tail = tmp;
            tmp->n = NULL;
        }
        list->third=list->head->n->n;
    }
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
        list->third=list->head->n->n;
    }
}

llnode* find(llist* list, int n)
{
    llnode* tmp = list->head;
    while( tmp != NULL && tmp->v != n )
    {
        tmp = tmp->n;
    }
    return tmp;
}

llnode* at(llist* list, unsigned long long n)
{
    unsigned long long i = 0;
    llnode* tmp = list->head;
    while( tmp != NULL && i < n )
    {
        tmp = tmp->n;
    }
    return tmp;
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

int min_val(llist* list)
{
    int m = 2147483647;
    llnode* tmp = list->head;
    while( tmp != NULL )
    {
        if( tmp->v < m ) m = tmp->v;
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
        list->third=list->head->n->n;
        list->size += 3u;

        if( list->tail == node )
        {
            list->tail = ctail;
        }

        return 1;
    }
    return 0;
}

int insert_at_val(llist* list, llnode* chain, int val)
{
    llnode* tmp = list->head;
    llnode* ctail = chain;
    while( ctail->n != NULL ) ctail=ctail->n;
    while( tmp != NULL && tmp->v != val )
    {
        tmp=tmp->n;
    }

    if( tmp != NULL )
    {
        ctail->n=tmp->n;
        tmp->n=chain;
        list->third=list->head->n->n;
        list->size += 3u;

        if( list->tail == tmp )
        {
            list->tail = ctail;
        }

        return 1;
    }
    return 0;
}

void delete(llist** list)
{ 
    llnode* tmp = (*list)->head;
    while( (*list)->head != NULL )
    {
        tmp = (*list)->head;
        (*list)->head = (*list)->head->n;
        free(tmp);
    }
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

int mod(int x, int n)
{
    while( x < 0 ) x = n+x;
    return x % n;
}

void move( llist* list, int minv, int maxv, llnode** direct )
{
    roll_lft(list);

    llist pickup;
    pickup.head = remove_front3(list);
    pickup.tail = pickup.head->n->n;
    pickup.size = 3;

    int dst = mod(list->tail->v - 2,maxv)+1;

    while( find(&pickup,dst) != NULL )
    {
        dst = mod(dst - 2,maxv)+1;
    }

    insert_at_node(list,direct[dst-1],pickup.head);
}

llnode* direct[1000000];

int main(int argc, char** argv)
{
    llist* list = NULL;
    llnode* tmp = NULL;

    if( argc != 3 )
    {
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
        count = 1000000;
        steps = 10000000;
    }

    list = init();

    for( int i = 0; i < nums; ++i )
    {
        int input = argv[1][i]-48;
        tmp = push(list,input);
        direct[input-1] = tmp;
    }

    llnode* one = direct[0];

    if( one == NULL )
    {
        printf("ERR: The value '1' must appear in the input string\n");
        delete(&list);
        return 0;
    } 

    int maxv = max_val(list);
    int minv = min_val(list);

    int i = maxv;
    while (i < count)
    {
        i++;
        tmp = push(list,i);
        direct[i-1] = tmp;
    } 

    maxv = count;

    for( int i = 0; i < steps; ++i )
    {
        move(list,minv,maxv,direct);
    }

    if( part == 1 )
    {
        print_n_from(list,one->n,8);
    }
    else
    {
        printf("%lld\n", (long long)one->n->v * (long long)one->n->n->v );
    }

    delete(&list);
    
    return 0;
}