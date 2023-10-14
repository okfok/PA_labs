#include <iostream>
#include <fstream>
#include <cmath>
#include <chrono>

const std::string INPUT_FILE_NAME = "data.bin";
const int M = 3;
const long long N = pow(2, 16);

long long fib(long long n) {
    if (n <= 2)
        return 1;
    else
        return fib(n - 1) + fib(n - 2);
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

void merge(std::string in1, std::string in2, std::string out, long long c1, long long c2, bool second_is_longer) {
    std::fstream fin1(in1, std::fstream::in | std::ios::binary);
    std::fstream fin2(in2, std::fstream::in | std::ios::binary);
    std::ofstream fout(out, std::ios::binary);


    int num1, num2, last = 0;
    long long n1 = 1, n2 = 1;
    fin1.read((char *) &num1, sizeof(int));
    fin2.read((char *) &num2, sizeof(int));


    while (true) {
        if ((last <= num1 && num1 <= num2) || (num1 <= num2 && num2 < last) || (num2 < last && last <= num1)) {
            fout.write((char *) (&num1), sizeof(int));
            last = num1;
            if (n1 < c1 * N) {
                fin1.read((char *) &num1, sizeof(int));
                n1++;
            } else
                break;
        } else if ((last <= num2 && num2 < num1) || (num2 < num1 && num1 < last) || (num1 < last && last <= num2)) {
            fout.write((char *) (&num2), sizeof(int));
            last = num2;
            if (n2 < c2 * N) {
                fin2.read((char *) &num2, sizeof(int));
                n2++;
            } else
                break;
        } else
            throw std::invalid_argument(std::to_string(last)+ " - " + std::to_string(num1) + " - " + std::to_string(num2));


    }


    if (n1 < c1 * N) {
        for (long long i = 0; i <= c1 * N - n1; ++i) {
            fout.write((char *) (&num1), sizeof(int));
            fin1.read((char *) &num1, sizeof(int));

        }
    }

    if (n2 < c2 * N) {
        for (long long i = 0; i <= c2 * N - n2; ++i) {
            fout.write((char *) (&num2), sizeof(int));
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
    fout.close();
}

void task(std::string file_name) {
    std::ifstream file(file_name, std::ios::binary);
    std::ofstream part1("1", std::ios::binary);
    std::ofstream part2("2", std::ios::binary);

    int j = 0, p1 = 0, p2 = 0;
    while (!file.eof()) {
        j++;
        long long n = fib(j) - ((j % 2) ? p1 : p2);
        for (long long i = 0; i < n; ++i) {


            int nums[N];
            file.read((char *) &nums, sizeof(nums));
            if (file.eof())
                break;

            quickSort(nums, 0, N - 1);

            if (j % 2) {
                part1.write((char *) (&nums), sizeof(nums));
                p1++;
            } else {
                part2.write((char *) (&nums), sizeof(nums));
                p2++;
            }


        }
    }


    part1.close();
    part2.close();
    file.close();


    int count[M] = {p1, p2, 0};
    int len[M] = {1, 1, 0};

    while (count[0] + count[1] + count[2] != 1) {
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


    if (count[0] == 1){
        rename("1", "result.bin");
        remove("2");
        remove("3");
    }

    if (count[1] == 1){
        rename("2", "result.bin");
        remove("1");
        remove("3");
    }

    if (count[2] == 1){
        rename("3", "result.bin");
        remove("2");
        remove("1");
    }


}


int main() {
    std::ofstream f;
    f.open("1", std::fstream::out | std::ios::binary | std::ios::trunc);
    f.close();
    f.open("2", std::fstream::out | std::ios::binary | std::ios::trunc);
    f.close();
    f.open("3", std::fstream::out | std::ios::binary | std::ios::trunc);
    f.close();
//
//    create_unsorted_file(INPUT_FILE_NAME);
//    print_file(INPUT_FILE_NAME);
//
    auto start = std::chrono::system_clock::now();
    task(INPUT_FILE_NAME);
    auto end = std::chrono::system_clock::now();


    std::chrono::duration<double> elapsed_seconds = end-start;
    std::time_t end_time = std::chrono::system_clock::to_time_t(end);
    std::cout << elapsed_seconds.count();


//    print_file("result.bin");



}

