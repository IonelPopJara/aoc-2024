#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define HASH_SIZE 1000000

int count_digits(int number) {
    if (number < 0) {
        return -1;
    }

    char buffer[20];
    snprintf(buffer, sizeof(buffer), "%d", number);
    return strlen(buffer);
}

size_t get_disk_size(int* file_block_sizes, int* free_block_sizes) {
    // 12345
    // 0..111....22222
    // size = 15
    size_t size = 0;
    for (int i = 0; i < HASH_SIZE; i++) {
        if (file_block_sizes[i] > 0) {
            // Acount for IDs with more than 1 digit
            size_t id_size = count_digits(i);
            size += (file_block_sizes[i] * id_size);
        }

        if (free_block_sizes[i] > 0) {
            size += free_block_sizes[i];
        }
    }

    return size;
}

char* insert_string(char* original, char* insert, size_t position) {
    // Check if the insert position is valid
    if (position > strlen(original)) {
        printf("ERROR! <position> needs to be less than length\n");
        return NULL;
    }

    // insert_string("program", "dog", 2) -> "prodoggram"
    size_t new_size = strlen(original) + strlen(insert) + 1;
    char* new_str = (char*)calloc(new_size, sizeof(char));

    size_t index = 0;
    while (index < position) {
        new_str[index] = original[index];
        index++;
    }

    for (int i = 0; i < strlen(insert); i++) {
        new_str[index++] = insert[i];
    }

    for (int i = position + 1; i < strlen(original); i++) {
        new_str[index++] = original[i];
    }

    return new_str;
}

char* remove_string(char* original, size_t remove_length, size_t position) {
    // original = 101010
    // remove = 10
    // position = 2
    // return -> 10.10
    size_t new_size = strlen(original) - remove_length + 1;
    char* new_str = (char*)calloc(new_size, sizeof(char));

    size_t index = 0;
    while (index < position) {
        new_str[index] = original[index];
        index++;
    }

    int restart = index + remove_length;

    new_str[index++] = '.';

    while (index < new_size) {
        new_str[index] = original[restart];
        index++;
        restart++;
    }

    return new_str;
}

int main(int argc, char** argv) {

    if (argc < 2) {
        printf("Usage day-09 <file_path>\n");
        return 0;
    }

    // Open file
    printf("Opening file...\n");

    char* original = "00...111...2...333.44.5555.6666.777.888899.101010";
    size_t remove_length = 2;
    char* test = remove_string(original, remove_length, 47);
    printf("Original:\t%s\n", original);
    printf("Remove: \t%s\n", test);

    char input_file[1024];
    snprintf(input_file, sizeof(input_file), "%sinput-01.txt", argv[1]);

    FILE* fd;

    if ((fd = fopen(input_file, "r")) == NULL) {
        fprintf(stderr, "ERROR. [%s] could not be opened.\n", input_file);
        return 1;
    }

    printf("[%s] opened successfully!\n", input_file);

    // ---- START PROCESS FILE DATA ----
    printf("Processing input...\n");

    // This array will work as a hashmap to store the sizes per block ID
    int file_block_sizes[HASH_SIZE] = { 0 };
    // Similarly, this array will store the free blocks
    int free_block_sizes[HASH_SIZE] = { 0 };

    /*
     * `reading_state` is a flag.
     *      : 0 => reading block file
     *      : 1 => reading free space
     */
    int reading_state = 0; // Initialize reading state
    unsigned long current_id = 0;

    char buffer[2048];
    printf("Disk: ");
    while (fgets(buffer, sizeof(buffer), fd) != NULL) {
        // Remove trailing newline, if present
        int len = strlen(buffer);
        if (len > 0 && buffer[len - 1] == '\n') {
            buffer[len - 1] = '\0';
        }

        // Check 
        printf("%s", buffer);
        char* c = buffer;
        while (*c != '\0') {
            // No error checking, I'll assume that we can only have numbers
            int block_counter = *c - '0';

            /*printf("%d | ID: %lu | Counter: %d\n", *c - '0', current_id, block_counter);*/

            if (reading_state == 0) {
                file_block_sizes[current_id] = block_counter;
            } else if (reading_state == 1) {
                free_block_sizes[current_id] = block_counter;
                current_id++;
            }

            // toggle reading state for next iteration
            reading_state = reading_state == 0 ? 1 : 0;

            c++;
        }
    }

    printf("\n");

    printf("Disk hashmaps:\n");
    for (int i = 0; i < HASH_SIZE; i++) {
        if (file_block_sizes[i] > 0) {
            printf("\tID: %d | Block: %d | Free: %d\n", i, file_block_sizes[i], free_block_sizes[i]);
        }
    }

    size_t disk_size = get_disk_size(file_block_sizes, free_block_sizes);

    int* disk_map_array = (int*)calloc(disk_size, sizeof(int));
    // Initialize disk array
    for (int i = 0; i < disk_size; i++) {
        disk_map_array[i] = -1;
    }

    printf("Expanded disk map:\n");
    printf("\tSize: %lu\n", disk_size);

    size_t current_size = 0;
    size_t max_size = 10000;
    char str_id[max_size];
    size_t array_size = 0;

    for (int id = 0; id < HASH_SIZE; id++) {
        if (file_block_sizes[id] > 0) {
            // Convert the id to string
            sprintf(str_id, "%d", id);
            for (int j = 0; j < file_block_sizes[id]; j++) {
                disk_map_array[array_size++] = id;
            }
        }

        if (free_block_sizes[id] > 0) {
            for (int j = 0; j < free_block_sizes[id]; j++) {
                disk_map_array[array_size++] = -1;
            }
        }
    }

    printf("\tStr: ");
    for (int i = 0; i < disk_size; i++) {
        if (disk_map_array[i] == -1) {
            printf(".");
        } else {
            printf("%d", disk_map_array[i]);
        }
    }
    printf("\n");


    // Move file blocks
    int left = 0;
    int right = disk_size - 1;

    while (left < right) {
        while (disk_map_array[left] != -1) left++;

        while (disk_map_array[right] == -1) right--;

        if (left >= right) break;

        // Swap elements
        disk_map_array[left] = disk_map_array[right];
        disk_map_array[right] = -1;
    }

    printf("Compacted disk map:\n");
    printf("\tSize: %lu\n", disk_size);
    printf("\tStr: ");
    for (int i = 0; i < disk_size; i++) {
        if (disk_map_array[i] == -1) {
            printf(".");
        } else {
            printf("%d", disk_map_array[i]);
        }
    }
    printf("\n");

    // Checksum
    unsigned long checksum = 0;
    for (size_t i = 0; i < disk_size; i++) {
        if (disk_map_array[i] < 0) break;
        checksum += i * disk_map_array[i];
    }

    printf("Checksum:\n");
    printf("\t%lu\n", checksum);

    // ---- END PROCESS FILE DATA ----

    printf("Finish program...\n");
    // Close file
    fclose(fd);

    // Finish the program
    return 0;
}
