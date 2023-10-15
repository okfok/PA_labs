#include <iostream>
#include <fstream>
#include <cmath>
#include <chrono>

const std::string INPUT_FILE_NAME = "data.bin";
const std::string OUTPUT_FILE_NAME = "result.bin";
const int M = 5;
const int N = pow(2, 16);
const char *TEMP_FILE_NAMES[] = {"1", "2", "3", "4", "5"};

long long fib(long long n) {
    if (n <= 4)
        return 1;
    else
        return fib(n - 1) + fib(n - 2) + fib(n - 3) + fib(n - 4);
}


inline long long min(int n1, int n2) { return (n1 < n2) ? n1 : n2; }

int partition(int arr[], int start, int end) {

    int pivot = arr[start];

    int count = 0;
    for (int i = start + 1; i <= end; i++) {
        if (arr[i] <= pivot)
            count++;
    }

    // Giving pivot element its correct position
    int pivotIndex = start + count;
    std::swap(arr[pivotIndex], arr[start]);

    // Sorting left and right parts of the pivot element
    int i = start, j = end;

    while (i < pivotIndex && j > pivotIndex) {

        while (arr[i] <= pivot) {
            i++;
        }

        while (arr[j] > pivot) {
            j--;
        }

        if (i < pivotIndex && j > pivotIndex) {
            std::swap(arr[i++], arr[j--]);
        }
    }

    return pivotIndex;
}

void quickSort(int arr[], int start, int end) {

    // base case
    if (start >= end)
        return;

    // partitioning the array
    int p = partition(arr, start, end);

    // Sorting the left part
    quickSort(arr, start, p - 1);

    // Sorting the right part
    quickSort(arr, p + 1, end);
}

void create_unsorted_file(std::string file_name) {
    std::ofstream file(file_name, std::ios::binary);
    long long len = pow(2, 20) * fib(10);
    for (long long i = 0; i < len; ++i) {
        int num = rand();
        file.write((char *) (&num), sizeof(num));

    }

    file.close();
}

void print_file(std::string file_name) {
    std::ifstream file(file_name, std::ios::binary);

    while (true) {
        int num;
        file.read((char *) &num, sizeof(num));
        if (file.eof())
            break;
        std::cout << num << ' ';
    }
    std::cout << '\n';
    file.close();
}

void pp() {
    std::cout << "-------------1\n";
    print_file("1");
    std::cout << "-------------2\n";
    print_file("2");
    std::cout << "-------------3\n";
    print_file("3");
}

void merge(const int in_files[], int out_file) {
    std::fstream files[M - 1];

    for (int i = 0; i < M - 1; ++i) {
        files[i].open(TEMP_FILE_NAMES[in_files[i]], std::fstream::in | std::ios::binary);
    }

    std::ofstream out(TEMP_FILE_NAMES[out_file], std::ios::binary);


    int last = 0, nums[M - 1], used[M - 1];
    for (int i = 0; i < M - 1; ++i) {
        files[i].read((char *) &nums[i], sizeof(int));
        used[i] = 1;
    }


    while (true) {
        if ((last <= num1 && num1 <= num2) || (num1 <= num2 && num2 < last) || (num2 < last && last <= num1)) {
            out.write((char *) (&num1), sizeof(int));
            last = num1;
            if (n1 < c1 * N) {
                fin1.read((char *) &num1, sizeof(int));
                n1++;
            } else
                break;
        } else if ((last <= num2 && num2 < num1) || (num2 < num1 && num1 < last) || (num1 < last && last <= num2)) {
            out.write((char *) (&num2), sizeof(int));
            last = num2;
            if (n2 < c2 * N) {
                fin2.read((char *) &num2, sizeof(int));
                n2++;
            } else
                break;
        } else
            throw std::invalid_argument(
                    std::to_string(last) + " - " + std::to_string(num1) + " - " + std::to_string(num2));


    }


    if (n1 < c1 * N) {
        for (long long i = 0; i <= c1 * N - n1; ++i) {
            out.write((char *) (&num1), sizeof(int));
            fin1.read((char *) &num1, sizeof(int));

        }
    }

    if (n2 < c2 * N) {
        for (long long i = 0; i <= c2 * N - n2; ++i) {
            out.write((char *) (&num2), sizeof(int));
            fin2.read((char *) &num2, sizeof(int));

        }
    }


    if (second_is_longer) {
        fin1.close();
        fin1.open(in1, std::fstream::out | std::ios::binary);
        while (true) {
            if (last == num2)
                fin2.read((char *) &num2, sizeof(int));

            if (fin2.eof())
                break;
            fin1.write((char *) (&num2), sizeof(int));
            fin2.read((char *) &num2, sizeof(int));
        }
        fin2.close();
        fin2.open(in2, std::fstream::out | std::ios::binary | std::ios::trunc);
    } else {
        fin2.close();
        fin2.open(in2, std::fstream::out | std::ios::binary);
        while (true) {
            if (last == num1)
                fin1.read((char *) &num1, sizeof(int));

            if (fin1.eof())
                break;
            fin2.write((char *) (&num1), sizeof(int));
            fin1.read((char *) &num1, sizeof(int));
        }
        fin1.close();
        fin1.open(in1, std::fstream::out | std::ios::binary | std::ios::trunc);
    }


    fin1.close();
    fin2.close();
    out.close();
}

void task(std::string file_name) {
    std::ifstream input(file_name, std::ios::binary);
    std::ofstream temp_files[M - 1];
    int j = 0;
    int count[M];
    for (int i = 0; i < M - 1; ++i) {
        temp_files[i].open(TEMP_FILE_NAMES[i], std::ios::binary);
        count[i] = 0;
    }

    while (!input.eof()) {
        j++;
        long long n = fib(j) - count[j % (M - 1)];
        for (long long i = 0; i < n; ++i) {


            int nums[N];
            input.read((char *) &nums, sizeof(nums));
            if (input.eof())
                break;

            quickSort(nums, 0, N - 1);


            temp_files[j % (M - 1)].write((char *) (&nums), sizeof(nums));
            count[j % (M - 1)]++;


        }
    }


    for (auto &file: temp_files) {
        file.close();
    }
    input.close();


    int len[M] = {1, 1, 1, 1, 0};

    while (count[0] + count[1] + count[2] + count[3] + count[4] != 1) {
//        pp();
        std::cout << "++\n" << len[0] << ' ' << len[1] << ' ' << len[2] << '\n' << count[0] << ' ' << count[1] << ' '
                  << count[2] << "\n++\n";
        if (count[0] == 0) {
            int m = min(count[1], count[2]);
            merge("2", "3", "1", m * len[1], m * len[2], count[1] < count[2]);
            count[0] = min(count[1], count[2]);
            len[0] = len[1] + len[2];

            if (count[1] < count[2]) {
                count[1] = abs(count[1] - count[2]);
                len[1] = len[2];
                count[2] = 0;
                len[2] = 0;
            } else {
                count[2] = abs(count[1] - count[2]);
                len[2] = len[1];
                count[1] = 0;
                len[1] = 0;
            }
        } else if (count[1] == 0) {
            int m = min(count[0], count[2]);
            merge("1", "3", "2", m * len[0], m * len[2], count[0] < count[2]);
            count[1] = min(count[0], count[2]);
            len[1] = len[0] + len[2];

            if (count[0] < count[2]) {
                count[0] = abs(count[0] - count[2]);
                len[0] = len[2];
                count[2] = 0;
                len[2] = 0;
            } else {
                count[2] = abs(count[0] - count[2]);
                len[2] = len[0];
                count[0] = 0;
                len[0] = 0;
            }
        } else if (count[2] == 0) {
            int m = min(count[0], count[1]);
            merge("1", "2", "3", m * len[0], m * len[1], count[0] < count[1]);
            count[2] = min(count[0], count[1]);
            len[2] = len[0] + len[1];

            if (count[0] < count[1]) {
                count[0] = abs(count[0] - count[1]);
                len[0] = len[1];
                count[1] = 0;
                len[1] = 0;
            } else {
                count[1] = abs(count[0] - count[1]);
                len[1] = len[0];
                count[0] = 0;
                len[0] = 0;
            }
        } else
            throw std::invalid_argument("2");
    }
//    pp();
//    std::cout << "++\n" << len[0] << ' ' << len[1] << ' ' << len[2] << '\n' << count[0] << ' ' << count[1] << ' '
//              << count[2] << "\n++\n";


    if (count[0] == 1) {
        rename("1",);
        remove("2");
        remove("3");
    }

    if (count[1] == 1) {
        rename("2", "result.bin");
        remove("1");
        remove("3");
    }

    if (count[2] == 1) {
        rename("3", "result.bin");
        remove("2");
        remove("1");
    }


}


int main() {
    std::ofstream f;
    for (auto &file_name: TEMP_FILE_NAMES) {
        f.open(file_name, std::fstream::out | std::ios::binary | std::ios::trunc);
        f.close();
    }
//
//    create_unsorted_file(INPUT_FILE_NAME);
//    print_file(INPUT_FILE_NAME);
//
    auto start = std::chrono::system_clock::now();
    task(INPUT_FILE_NAME);
    auto end = std::chrono::system_clock::now();


    std::chrono::duration<double> elapsed_seconds = end - start;
    std::time_t end_time = std::chrono::system_clock::to_time_t(end);
    std::cout << elapsed_seconds.count();


//    print_file("result.bin");



}

