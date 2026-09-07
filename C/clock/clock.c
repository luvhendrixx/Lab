#include <stdio.h>
#include <time.h>
#include <stdbool.h>
#include <unistd.h> // unix std -> provides the sleep func

int main(void) {
    time_t rawtime = 0;
    // we give it NULL cause we haven't found an address to give to it yet
    struct tm *pTime = NULL; // if we don't assing a value to a struct, it ought to hold garbage value...so we assign NULL meaning it should hold no value
    bool isRunning = true; // keeps the loop running indefinetly

    printf("DIGITAL CLOCK\n");

    while(isRunning) { // while is running == true...exe the code in the {}
        time(&rawtime); // grabs the raw sys time in seconds and overwrites the 0 we set above

        // takes the raw sec and auto converts them to my local timezone as well as breaks...
        // them into components (hours, min, seconds)...
        // and saves the organized data inside our pTime struct
        pTime = localtime(&rawtime); // now we can give pTime an address which "overwrites" the NULL

        // the ? is just shorthand if/else logic....
        // if the condition is true, it picks "PM"..
        // otherwise, "AM"
        // think of the pTime->tm_hour as..pulling a card (tm_hour) from a full pack of cards (pTime)
        // if u decided to not use the -> op, you'd have to write (*pTime).tm_hour
        char *am_pm = (pTime->tm_hour >= 12) ? "PM" : "AM";

        int hour12 = pTime->tm_hour % 12;
        if (hour12 == 0) {
            hour12 = 12; // change 0 to 12 for midnight and noon (we don't want to print 00)
        }
        // print the time
        printf("\r%02d:%02d:%02d %s", hour12, pTime->tm_min, pTime->tm_sec, am_pm);
        // flush the output out of buffer
        fflush(stdout);
        // we pause a sec cuz of CPU efficiency (the PC will display data at lightning speed and throtlle comp resources)
        // and for human readability (how can you read stuff going at the speed of light?)
        sleep(1); // DO NOT REMOVE AND RUN THE PROGRAMME WITHOUT THIS UNLESS YOU WANT TO CRASH YOUR PC!!..trust :-()
    }
    return 0;
}
