#include <vector>
#include <iostream>
#include <chrono>
#include <thread>
const int N = 10;

int main() {
    std::vector<int> arr(N);
    for(int i = 0; i < N; ++i) {
        arr[i] = i*i;
    }
    for(int i = 0; i < 10; ++i) {
        std::this_thread::sleep_for(std::chrono::milliseconds(10000));
        for(int v: arr) {
            std::cout << v << " ";
        }
    }
    return 0;
}