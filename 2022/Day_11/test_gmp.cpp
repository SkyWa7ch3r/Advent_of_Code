#include <gmpxx.h>
#include <iostream>
#include <vector>

int main(int argc, char* argv[]) {
    mpz_class bigNum{"100000000000000000000000000000000000000000000000000000000000000000000000000000"};
    mpz_class bigNum2{123456789};

    mpz_class multiplied;

    multiplied = bigNum * bigNum2;

    mpz_class rem{bigNum % 5};

    if(rem == 0) {
        std::cout << "rem == 0 is true\n";
    }

    std::cout << rem << " " << bigNum << "\n";

    std::cout << multiplied << (multiplied > bigNum ? " Multipled is larger than bigNum2 because duh" : "What?!") << "\n";

    std::cout << bigNum2 / 2 << "\n";

    std::vector<mpz_class> bigNumbers;

    bigNumbers.push_back(bigNum);
    bigNumbers.push_back(bigNum2);
    bigNumbers.push_back(multiplied);

    for (auto num: bigNumbers) {
        std::cout << num << "\n";
    }

    return 0;

}