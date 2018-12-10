#include <stdio.h>
#include <stdlib.h>

struct node;
struct node {
    struct node *next;
    long int value;
};

static struct node** buckets;

static int check_freq(long int freq) {
    uint8_t bucket_idx = freq & 0xFF;
    struct node* n = buckets[bucket_idx];
    if (n == NULL) {
        buckets[bucket_idx] = n = calloc(1, sizeof(struct node));
        n->value = freq;
        return 0;
    }
    do {
        if(n->value == freq) return 1;
        if(!n->next) {
            n->next = calloc(1, sizeof(struct node));
            n->next->value = freq;
            return 0;
        }
        n = n->next;
    }
    while(n != NULL);
}

int main() {
    buckets = calloc(256, sizeof(struct node*));

    FILE *f = fopen("input-day1.txt", "r");
    long int freq = 0;
    for(;;) {
        char l[128];
        if(!fgets(l, 128, f)) {
            fseek(f, 0, 0);
            continue;
        }
        long int delta = strtol(l, NULL, 10);
        freq += delta;
        if(check_freq(freq)) break;
    }
    printf("%ld\n", freq);
}