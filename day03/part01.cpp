#include <algorithm>
#include <fstream>
#include <iostream>
#include <string>
#include <cstdlib>
#include <ranges>

int main(int const argc, char const * const * const argv) {
    if (argc != 2) {
        std::cerr << "Usage: " << argv[0] << " <filename>\n";
        std::exit(EXIT_FAILURE);
    }
    auto const filename = argv[1];
    auto file = std::ifstream{ filename };
    if (not file) {
        std::cerr << "Failed to open file '" << filename << '\n';
        std::exit(EXIT_FAILURE);
    }

    auto line = std::string{};
    auto total = 0uz;
    while (std::getline(file, line)) {
        auto max_joltage = 0;
        for (auto const i : std::views::iota(0uz, line.length())) {
            for (auto const j : std::views::iota(i + 1, line.length())) {
                auto const joltage = 10 * (line.at(i) - '0') + (line.at(j) - '0');
                max_joltage = std::max(max_joltage, joltage);
            }
        }
        // std::cout << max_joltage << '\n\n';
        total += static_cast<std::size_t>(max_joltage);
    }

    std::cout << "total: " << total << '\n';
}