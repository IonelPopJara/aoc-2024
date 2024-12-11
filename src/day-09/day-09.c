#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_ID 1000000
#define MAX_BLOCKS 100000

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
    for (int i = 0; i < MAX_ID; i++) {
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

size_t checksum(int* disk_map, size_t disk_size) {
    unsigned long checksum = 0;
    for (size_t i = 0; i < disk_size; i++) {
        if (disk_map[i] >= 0) {
            checksum += i * disk_map[i];
        }
    }
    return checksum;
}

void print_array(size_t* disk_spaces, size_t length) {
    for (size_t i = 0; i < length; i++) {
        if (disk_spaces[i] == -1) {
            break;
        }

        printf("%lu", disk_spaces[i]);
    }
    printf("\n");
}

/*
 * `reading_state` is a flag.
 *      : 0 => reading block file
 *      : 1 => reading free space
 */
size_t* get_disk_block_sizes(int file_block_sizes[MAX_ID], int free_block_sizes[MAX_ID], FILE* fd, size_t* length) {

    int reading_state = 0; // Initialize reading state
    unsigned long current_id = 0; // Initialize current id to store the data

    char buffer[2048];
    *length = 0;

    while (fgets(buffer, sizeof(buffer), fd) != NULL) {
        // Remove trailing newline, if present
        int len = strlen(buffer);
        if (len > 0 && buffer[len - 1] == '\n') {
            buffer[len - 1] = '\0';
        }

        // Check 
        /*printf("%s", buffer);*/
        char* c = buffer;
        while (*c != '\0') {
            *length = *length + 1;
            // No error checking, I'll assume that we can only have numbers
            int block_counter = *c - '0';

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

    rewind(fd);

    // Disk spaces
    size_t* disk_spaces = (size_t*)calloc(*length, sizeof(size_t));

    // Do it again because I don't wanna deal with dynamic arrays
    while (fgets(buffer, sizeof(buffer), fd) != NULL) {
        // Remove trailing newline, if present
        int len = strlen(buffer);
        if (len > 0 && buffer[len - 1] == '\n') {
            buffer[len - 1] = '\0';
        }

        for (size_t i = 0; i < *length; i++) {
            disk_spaces[i] = -1;
        }

        char* c = buffer;
        c = buffer;
        size_t index = 0;
        while (*c != '\0') {
            /*printf("c: %c\n", *c);*/
            disk_spaces[index] = *c - '0';
            c++;
            index++;
        }
    }

    return disk_spaces;
}

void print_disk_block_sizes(int file_block_sizes[MAX_ID], int free_block_sizes[MAX_ID]) {
    for (int i = 0; i < MAX_ID; i++) {
        if (file_block_sizes[i] > 0) {
            printf("\tID: %d | Block: %d | Free: %d\n", i, file_block_sizes[i], free_block_sizes[i]);
        }
    }
}

void print_disk_map(int* disk_map, size_t disk_size) {
    printf("\tStr: ");
    for (int i = 0; i < disk_size; i++) {
        if (disk_map[i] == -1) {
            printf(".");
        } else {
            printf("%d", disk_map[i]);
        }
    }
    printf("\n");
}

int* get_disk_map(int file_block_sizes[MAX_ID], int free_block_sizes[MAX_ID], size_t* disk_size) {
    *disk_size = get_disk_size(file_block_sizes, free_block_sizes);

    int* disk_map = (int*)calloc(*disk_size, sizeof(int));
    // Initialize disk array
    for (int i = 0; i < *disk_size; i++) {
        disk_map[i] = -1;
    }

    printf("Expanded disk map:\n");
    printf("\tSize: %lu\n", *disk_size);

    size_t current_size = 0;
    size_t max_size = 10000;
    char str_id[max_size];
    size_t array_size = 0;

    for (int id = 0; id < MAX_ID; id++) {
        if (file_block_sizes[id] > 0) {
            for (int j = 0; j < file_block_sizes[id]; j++) {
                disk_map[array_size++] = id;
            }
        }

        if (free_block_sizes[id] > 0) {
            for (int j = 0; j < free_block_sizes[id]; j++) {
                disk_map[array_size++] = -1;
            }
        }
    }

    return disk_map;
}

size_t find_element_for_space(size_t spaces, int* disk_map, size_t disk_size, size_t* disk_spaces, size_t disk_spaces_length) {
    size_t spaces_index = disk_spaces_length - 1;
    size_t map_index = disk_size - 1;

    while (map_index >= 0) {
        printf("\t\tmap_index: %zu | spaces_index: %zu\n", map_index, spaces_index);
        printf("\t\t%map item: %d | space number : %zu\n", disk_map[map_index], disk_spaces[spaces_index]);
        size_t current = disk_map[map_index];
        size_t number_of_spaces = disk_spaces[spaces_index];
        if (current != -1) {

            printf("\t\tThere are %zu [%zu]s\n", number_of_spaces, current);
            // Find an element that has at least `number_of_spaces` number of spaces
            if (number_of_spaces <= spaces) {
                return map_index;
            }
        }

        map_index -= number_of_spaces;
        spaces_index-=1;
    }

    return -1;
}

int main(int argc, char** argv) {

    if (argc < 2) {
        printf("Usage day-09 <file_path>\n");
        return 0;
    }

    // ---- START OPEN FILE ----
    printf("Opening file...\n");

    char input_file[1024];
    snprintf(input_file, sizeof(input_file), "%sinput-02.txt", argv[1]);

    FILE* fd;
    if ((fd = fopen(input_file, "r")) == NULL) {
        fprintf(stderr, "ERROR. [%s] could not be opened.\n", input_file);
        return 1;
    }
    printf("[%s] opened successfully!\n", input_file);
    // ---- END OPEN FILE ----

    // ---- START PROCESS FILE DATA ----
    printf("Processing input...\n");

    // This array will store the file blocks per id
    int file_block_sizes[MAX_ID] = { 0 };
    // Similarly, this array will store the free blocks per id
    int free_block_sizes[MAX_ID] = { 0 };

    size_t disk_spaces_length;
    size_t* disk_spaces = get_disk_block_sizes(file_block_sizes, free_block_sizes, fd, &disk_spaces_length);
    printf("Input:\t");
    print_array(disk_spaces, disk_spaces_length);

    printf("Disk Block Sizes:\n");
    print_disk_block_sizes(file_block_sizes, free_block_sizes);
    // ---- END PROCESS FILE DATA ----

    // ---- START MAP VALUES ----
    size_t disk_size;
    int* disk_map = get_disk_map(file_block_sizes, free_block_sizes, &disk_size);
    print_disk_map(disk_map, disk_size);

    // ---- END MAP VALUES ----

    // ---- START DISK FRAGMENTATION ----
    printf("Fragmentation:\n");
    size_t spaces_index = 0;
    size_t map_index = 0;
    while (map_index < disk_size) {
        size_t current = disk_map[map_index];
        size_t number_of_spaces = disk_spaces[spaces_index];
        if (current == -1) {
            printf("Insert %zu blocks here! [%zu]\n", disk_spaces[spaces_index], map_index);

            // Find an element that has `number_of_spaces` number of spaces
            size_t found_index = find_element_for_space(number_of_spaces, disk_map, disk_size, disk_spaces, disk_spaces_length);
            printf("[%d] can be inserted here\n", disk_map[found_index]);
        }

        map_index += number_of_spaces;
        spaces_index+=1;
    }

    /*printf("Fragmentation:\n");*/
    /*size_t spaces_index = 0;*/
    /*size_t map_index = 0;*/
    /*while (map_index < disk_size) {*/
    /*    size_t current = disk_map[map_index];*/
    /*    size_t spaces = disk_spaces[spaces_index];*/
    /*    if (current != -1) {*/
    /*        printf("There are %zu blocks of '%zu's here.\n", disk_spaces[spaces_index], current);*/
    /*    }*/
    /*    else {*/
    /*        printf("There are %zu 'EMPTY' blocks here.\n", disk_spaces[spaces_index]);*/
    /*    }*/
    /**/
    /*    map_index += spaces;*/
    /*    spaces_index+=1;*/
    /*}*/

    return 0;
    // ---- END DISK FRAGMENTATION ----

    // ---- START CHECKSUM ----
    size_t final_checksum = checksum(disk_map, disk_size);

    printf("Checksum:\n");
    printf("\t%lu\n", final_checksum);
    // ---- END CHECKSUM ----

    printf("Finish program...\n");
    // Close file
    fclose(fd);

    // Finish the program
    return 0;
}
