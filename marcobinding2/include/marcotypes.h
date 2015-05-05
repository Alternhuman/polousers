#ifndef MARCO_TYPES_H
#define MARCO_TYPES_H

struct node
{
	char address[50];
	char* params;
};

typedef struct node marco_node;

#endif