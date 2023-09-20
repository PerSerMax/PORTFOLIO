#include <iostream>
#include <fstream>

typedef char ltype;

struct elem {
private:
    ltype data = NULL;
    elem* next = NULL;
public:
    elem() {};
    elem(ltype d) {
        data = d;
    }
    elem(ltype d, elem* n) {
        data = d;
        next = n;
    }

    ltype get_data() {
        return data;
    }
    elem* get_next() {
        return next;
    }
    void set_data(ltype data) {
        this->data = data;
    }
    void set_next(elem* next) {
        this->next = next;
    }

};

struct list {
private:
    elem* first = new elem;
    elem* last = new elem;
public:
    list() {
        first->set_next(last);
    }
    list(ltype str[]) {
        first->set_next(last);
        elem* ptr = this->first->get_next();
        for (size_t i = 0; str[i] != '\0'; i++)
        {
            ptr->set_data(str[i]);
            ptr->set_next(new elem);
            ptr = ptr->get_next();
        }
        this->last = ptr;
    }
    ~list() {
        elem* ptr1 = first;
        elem* ptr2 = NULL;
        for (size_t i = 0; ptr1 != NULL; i++)
        {
            ptr2 = ptr1;
            ptr1 = ptr1->get_next();
            delete ptr2;
        }
    }

    void print() {
        elem* ptr = this->first;
        for (size_t i = 0; ptr != NULL; i++)
        {
            std::cout << ptr->get_data();
            ptr = ptr->get_next();
        }
        std::cout << std::endl;
    }
    void del_seq(ltype seq[], size_t len) {
        elem* ptr = first;
        elem* tmp = NULL;
        elem* prev = NULL;
        for (size_t i = 0; ptr->get_next() != NULL; )
        {
            if (ptr->get_data() == seq[i]) {
                i++;
                if (i == len) {             
                    i = 0;
                    ptr = prev->get_next();
                    for (size_t j = 0; j < len; j++)
                    {
                        tmp = ptr;
                        ptr = ptr->get_next();
                        delete tmp;
                    }
                    prev->set_next(ptr);
                    prev = ptr;
                    continue;
                }
            }
            else {
                i = 0;
            }
            if (i == 0) {
                prev = ptr;
            }
            ptr = ptr->get_next();
        }
        this->last = ptr;
    }
    void add(ltype e) {
        last->set_data(e);
        last->set_next(new elem);
        last = last->get_next();
    }
};


void text_from_file(list* l, char file_name[]) {
    std::ifstream f;
    f.open(file_name);
    char c;
    while (true) {
        f.read(&c, 1);
        l->add(c);
        if (f.eof()) {
            break;
        }
    }
}

int main()
{
    using namespace std;
    char file[] = "C:\\Users\\max\\source\\repos\\ConsoleApplication\\ConsoleApplication\\file.txt";
    list l;
    for (size_t i = 0; file[i] != '\0'; i++)
    {
        l.add(file[i]);
    }
    l.print();
}
