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

//DECIMAL BEGIN

struct decimal {
	vector data;
	short sign;
};

typedef struct decimal decimal;

decimal new_decimal() {
	decimal a;
	a.data = new_vector();
	a.sign = 0;
	return a;
}

decimal to_decimal(long long a) {
	decimal d = new_decimal();
	if (a > 0) {
		d.sign = 1;
	}
	else if (a < 0) {
		d.sign = -1;
	}
	else {
		d.sign = 0;
		push_back(&(d.data), 0);
		return d;
	}
	do {
		push_back(&(d.data), a % 65536);
		a /= 65536;
	} while (a >= 1);
	return d;
}

void delete_decimal(decimal* d) {
	delete_vector(&(d->data));
	d->sign = 0;
}

// a > b = 1   |   a < b = -1   |   a == b = 0
short compare_decimal(decimal* a, decimal* b) {
	if (a->sign == 1 && b->sign == -1) {
		return 1;
	}
	else if (a->sign == -1 && b->sign == 1) {
		return -1;
	}
	if (a->data.loaded > b->data.loaded) {
		return 1;
	}
	else if (a->data.loaded < b->data.loaded) {
		return -1;
	}
	for (size_t i = a->data.loaded; i > 0; i--)
	{
		if (a->data.v_data[i - 1] > b->data.v_data[i - 1]) {
			return 1;
		}
		else if (a->data.v_data[i - 1] < b->data.v_data[i - 1]) {
			return -1;
		}
	}
	return 0;
}

void print_decimal(decimal* d) {
	if (d->sign == -1) {
		printf("-");
	}
	else {
		printf(" ");
	}
	for (size_t i = 1; i <= d->data.loaded; i++)
	{
		printf("%d ", d->data.v_data[d->data.loaded-i]);
	}
	printf("\n");
}

decimal d_sum(decimal* d1, decimal* d2) {
	decimal d3 = new_decimal();
	if (d1->data.loaded > d2->data.loaded) {
		for (size_t i = 0; i < d1->data.loaded; i++)
		{
			push_back(&d3, d1->data.v_data[i]);
		}
		for (size_t i = 0; i < d2->data.loaded; i++)
		{
			if ((V_TYPE)(d3.data.v_data[i] + d2->data.v_data[i]) < d3.data.v_data[i] ||
				(V_TYPE)(d3.data.v_data[i] + d2->data.v_data[i]) < d2->data.v_data[i]) {
				if (i + 2 > d3.data.loaded) {
					push_back(&d3.data, 0);
				}
				d3.data.v_data[i + 1] += 1;
			}
			d3.data.v_data[i] += d2->data.v_data[i];
		}
	}
	else {
		for (size_t i = 0; i < d2->data.loaded; i++)
		{
			push_back(&d3, d2->data.v_data[i]);
		}
		for (size_t i = 0; i < d1->data.loaded; i++)
		{
			if ((V_TYPE)(d3.data.v_data[i] + d1->data.v_data[i]) < d3.data.v_data[i] ||
				(V_TYPE)(d3.data.v_data[i] + d1->data.v_data[i]) < d1->data.v_data[i]) {
				if (i + 2 > d3.data.loaded) {
					push_back(&d3.data, 0);
				}
				d3.data.v_data[i + 1] += 1;
			}
			d3.data.v_data[i] += d1->data.v_data[i];
		}
	}
	return d3;
}

decimal d_sub(decimal* d1, decimal* d2) {
	decimal d3 = new_decimal();
	short comp = compare_decimal(d1, d2);
	if (comp == 1)
	{
		d3.sign = 1;
		for (size_t i = 0; i < d1->data.loaded; i++)
		{
			push_back(&d3.data, d1->data.v_data[i]);
		}
		for (size_t i = 0; i < d2->data.loaded; i++)
		{
			if (d3.data.v_data[i] < d2->data.v_data[i])
			{
				d3.data.v_data[i + 1] -= 1;
			}
			d3.data.v_data[i] -= d2->data.v_data[i];
		}
		while (d3.data.v_data[d3.data.loaded - 1] == 0) {
			pop_back(&d3);
		}
		return d3;
	}
	else if (comp == -1) {
		d3.sign = -1;
		for (size_t i = 0; i < d2->data.loaded; i++)
		{
			push_back(&d3.data, d2->data.v_data[i]);
		}
		for (size_t i = 0; i < d1->data.loaded; i++)
		{
			if (d3.data.v_data[i] < d1->data.v_data[i])
			{
				d3.data.v_data[i + 1] -= 1;
			}
			d3.data.v_data[i] -= d1->data.v_data[i];
		}
		while (d3.data.v_data[d3.data.loaded - 1] == 0) {
			pop_back(&d3);
		}
		return d3;
	}
	else {
		push_back(&d3.data, 0);
		return d3;
	}
}

decimal d_mul(decimal* d1, decimal* d2) {
	decimal tmp1;
	for (size_t i = 0; i < d2->data.loaded; i++)
	{
		tmp1 = new_decimal();
		decimal* ptr1 = &tmp1;
		for (size_t j = 0; j < d2->data.v_data[i]; j++)
		{
			tmp1 = d_sum(&tmp1, d1);
			print_decimal(&tmp1);
		}
		for (size_t k = 0; k < i; k++)
		{
			//push_fwd(&tmp2, 0);
		}
	}
	
	return tmp1;
}

//DECIMAL END

#endif

int main() {
	decimal d1 = to_decimal(2);
	decimal d2 = to_decimal(2);
	print_decimal(&d1);
	print_decimal(&d2);
	//decimal d3 = d_mul(&d2, &d1);
	//print_decimal(&d3);
	decimal d = to_decimal(1);
	for (size_t i = 0; i < 65536; i++)
	{
		d = d_sum(&d, &d);
		print_decimal(&d);
		printf("%d\n", &d);
	}
	print_decimal(&d);
	system("pause");
	delete_decimal(&d);
	system("pause");
}
