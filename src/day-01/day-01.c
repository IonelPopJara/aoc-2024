#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define HASHMAP_SIZE 300000

void merge(int* input_array, int left, int middle, int right);
void mergesort(int* input_array, int left, int right);

int main(int argc, char** argv) {

    if (argc < 2) {
        printf("ERROR. Please provide the input file path.\n");
        return 0;
    }

    // Initialize a hash_map to find the similarty score for part 2
    int hash_map[HASHMAP_SIZE];
    for (int i = 0; i < HASHMAP_SIZE; i++) {
        hash_map[i] = 0;
    }

    /*const char* input_file = strcat(argv[1], "input-example.txt");*/
    /*const char* input_file = strcat(argv[1], "input-short.txt");*/
    const char* input_file = strcat(argv[1], "input.txt");

    int n_lines = 0;

    printf("Opening input...\n");

    FILE* fd;

    if ((fd = fopen(input_file, "r")) == NULL) {
        printf("ERROR. [%s] cannot be opened.\n", input_file);
        return 0;
    }

    printf("[%s] opened successfuly!\n", input_file);

    /* NOTE:
     *  I don't want to implement a dynamic array so I'll do two passess.
     *  One for counting the number of elements in the lists, and another
     *  one for allocating the elements in the arrays.
     */
    char buffer[256];
    while (fgets(buffer, sizeof(buffer), fd) != NULL) {
        n_lines++;
    }

    printf("[%s] has %d lines.\n", input_file, n_lines);

    // Reset the fd pointer back to the begining of the file
    rewind(fd);

    // Allocate memory for the left and right lists
    int* left_list = (int*)calloc(n_lines, sizeof(int));
    int* right_list = (int*)calloc(n_lines, sizeof(int));

    int counter = 0;
    while (fgets(buffer, sizeof(buffer), fd) != NULL) {
        int l, r;
        if (sscanf(buffer, "%d %d", &l, &r) == 2) {
            left_list[counter] = l;
            right_list[counter] = r;

            // Part 2: Add the right element to the hashmap
            hash_map[r] += 1;
        }
        counter++;
    }

    printf("\nLists...\n");
    for (int i = 0; i < 6; i++) {
        printf("L: %d | R: %d\n", left_list[i], right_list[i]);
    }
    printf("...\n\n");

    // Sort lists
    mergesort(left_list, 0, n_lines - 1);
    mergesort(right_list, 0, n_lines - 1);


    // Calculate the distance between nodes and sum it
    printf("Part 1: Calculating distances...\n");
    long total_distance = 0;
    for (int i = 0; i < n_lines; i++) {
        int distance = abs(right_list[i] - left_list[i]);

        total_distance += distance;
    }
    printf("\tTotal distance: %ld.\n", total_distance);

    printf("Part 2: Calculating similarity score...\n");
    long total_similarity = 0;
    for (int i = 0; i < n_lines; i++) {
        int multiplier = hash_map[left_list[i]];
        int similarity = left_list[i] * multiplier;
        total_similarity += similarity;
    }
    printf("\tTotal similarity score: %ld.\n", total_similarity);

    fclose(fd);
    free(left_list);
    free(right_list);

    return 0;
}

void merge(int* input_array, int left, int middle, int right) {
    int n1 = middle - left + 1;
    int n2 = right - middle;

    // Copy the elements of the original array into the left and right sub-arrays
    int left_array[n1];
    for (int i = 0; i < n1; i++) {
        left_array[i] = input_array[left + i];
    }

    int right_array[n2];
    for (int j = 0; j < n2; j++) {
        right_array[j] = input_array[middle + 1 + j];
    }

    // Merge the elements by comparing them
    int i = 0;
    int j = 0;
    int k = left;
    while (i < n1 && j < n2) {
        if (left_array[i] < right_array[j]) {
            input_array[k] = left_array[i];
            i++;
        }
        else {
            input_array[k] = right_array[j];
            j++;
        }
        k++;
    }

    // Add the remaining elements if
    while (i < n1) {
        input_array[k++] = left_array[i++];
    }

    while (j < n2) {
        input_array[k++] = right_array[j++];
    }
}

void mergesort(int* input_array, int left, int right) {
    if (left >= right) {
        return;
    }

    int middle = left + (right - left) / 2;

    mergesort(input_array, left, middle);
    mergesort(input_array, middle + 1, right);
    merge(input_array, left, middle, right);

    return;
}
