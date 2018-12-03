#include <stdio.h>
#include <stdlib.h>

int main() {
    FILE *f = fopen("input-day1.txt", "r");
    long int freq = 0;
    while(!feof(f)) {
        char l[128];
        if(!fgets(l, 128, f)) break;
        long int delta = strtol(l, NULL, 10);
        freq += delta;
    }
    printf("%ld\n", freq);
}