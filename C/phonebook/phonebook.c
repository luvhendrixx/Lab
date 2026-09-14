#include <stdio.h>
#include <string.h>

typedef struct {
    char *name; // just holds a memory addr
    char *phone_num; // just holds a memory addr
} Contact;

int main(void) {
    // create an instance of the Contact struct
    Contact entry;

    // prompt the user for input...

    // 1. prompt for the name..scan it and place it in a regular string var

    // creating a user_name var
    char user_name[30]; // allocates room for a word upto 29 chars + the null terminator \0

    printf("Name? ");
    fgets(user_name, sizeof(user_name), stdin);
    user_name[strcspn(user_name, "\r\n")] = 0; // gets rid of that auto added newline made by fgets
    // scanf("%29s", user_name); // the %29s limits input to 29 chars, saving the 30th char for \0

    // 2. prompt for the phone_num...scan it and place it in a regular int var
    // the max std length for an international phone numnber is 15 digits (excluding the + sign or exit codes)
    char user_number[15];

    printf("Phone number? ");
    fgets(user_number, sizeof(user_number), stdin);
    user_number[strcspn(user_number, "\r\n")] = 0;
    //scanf("%14s", user_number);

    entry.name = user_name; // bc of array decay...we pass the mem addr of user_name inside the name struct
    entry.phone_num = user_number;

    printf("----- New contact added -------\n");
    printf("Name: %s\n", entry.name);
    printf("Phone number: %s\n", entry.phone_num);

    return 0;
}
