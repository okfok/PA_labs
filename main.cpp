#include <iostream>
#include <fstream>
#include <cmath>

const std::string INPUT_FILE_NAME = "data.bin";

void create_unsorted_file(std::string file_name) {
    std::ofstream file(file_name, std::ios::binary);

    for (int i = 0; i < pow(2, 3); ++i) {
        int num = rand() % 20;
        file.write((char *) (&num), sizeof(num));

    }

    file.close();
}

void print_file(std::string file_name) {
    std::ifstream file(file_name, std::ios::binary);

    while (!file.eof()) {
        int num;
        file.read((char *) &num, sizeof(num));
        std::cout << num << ' ';
    }
    std::cout << '\n';
    file.close();
}

void task(std::string file_name) {
    std::ifstream file(file_name, std::ios::binary);
    int m = 1;
    int last = 0;
    std::ofstream part(std::to_string(m), std::ios::binary);


    while (!file.eof()) {
        int num;
        file.read((char *) &num, sizeof(num));
        if (last <= num) {
            part.write((char *) (&num), sizeof(num));
        } else {
            part.close();
            m++;
            part.open(std::to_string(m), std::ios::binary);
            part.write((char *) (&num), sizeof(num));

        }

        last = num;
    }
    part.close();

    file.close();

    for (int i = 1; i <= m; ++i) {
        print_file(std::to_string(i));
    }


}


int main() {
    create_unsorted_file(INPUT_FILE_NAME);
    print_file(INPUT_FILE_NAME);
    task(INPUT_FILE_NAME);
}

