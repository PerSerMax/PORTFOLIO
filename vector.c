#ifndef VECTOR
#define VECTOR
#include <stdlib.h>
#include <stdio.h>
#include <math.h>

//VECTOR BEGIN

typedef unsigned short V_TYPE;

struct vector {
	unsigned int length;
	unsigned int loaded;
	V_TYPE* v_data;
};

typedef struct vector vector;

vector new_vector() {
	vector v;
	v.length = 2;
	v.loaded = 0;
	v.v_data = (V_TYPE*)calloc(2, sizeof(V_TYPE));
	return v;
}

void push_back(vector* v, V_TYPE d) {
	if (v->loaded + 1 > v->length) {
		V_TYPE* new_data = (V_TYPE*)realloc(v->v_data, 2 * sizeof(V_TYPE) * ((unsigned long long)(v->length)));
		if (!new_data) {
			printf("REALLOC ERROR");
			return;
		}
		v->length *= 2;
		v->v_data = new_data;
	}

	v->v_data[v->loaded] = d;
	v->loaded += 1;
}

void push_fwd(vector* v, V_TYPE d) {
	if (v->loaded + 1 > v->length) {
		V_TYPE* new_data = (V_TYPE*)realloc(v->v_data, 2 * sizeof(V_TYPE) * ((unsigned long long)(v->length)));
		if (!new_data) {
			printf("REALLOC ERROR");
			return;
		}
		v->length *= 2;
		v->v_data = new_data;
	}

	for (size_t i = v->loaded; i > 0; i--)
	{
		v->v_data[i] = v->v_data[i - 1];
	}
	v->v_data[0] = d;
	v->loaded += 1;
}

vector to_vector(unsigned long long len, V_TYPE* data) {
	vector v = new_vector();
	for (size_t i = 0; i < len; i++)
	{
		push_back(&v, data[i]);
	}
	return v;
}

void print_vector(vector* v) {
	for (unsigned long i = 0; i < v->loaded; i++)
	{
		printf("%d ", v->v_data[i]);
	}
	printf("\n");
}

void pop_back(vector* v) {
	v->v_data[v->loaded - 1] = 0;
	v->loaded -= 1;
	if (v->length / 2 >= v->loaded) {
		V_TYPE* new_data = (V_TYPE*)realloc(v->v_data, sizeof(V_TYPE) * ((unsigned long long)(v->length)) / 2);
		if (!new_data)
		{
			printf("CALLOC ERROR");
		}
		v->v_data = new_data;
		v->length /= 2;
	}
}

void delete_vector(vector* v) {
	free(v->v_data);
	v->v_data = NULL;
	v->length = 0;
	v->loaded = 0;
}

//VECTOR END

#endif
