#include <fstream>
#include <iostream>
#include <string>
#include <vector>

int main(int argc, char** argv) {
    if (argc < 2) {
        std::cerr << "No Input\n";
        return 1;
    }
    std::ifstream input{argv[1]};
    if (!input) {
        std::cerr << "File Couldn't be opened\n";
    }
    
    return 0;
}