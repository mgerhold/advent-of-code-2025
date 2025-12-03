#include <algorithm>
#include <fstream>
#include <iostream>
#include <string>
#include <cstdlib>
#include <cmath>
#include <ranges>
#include <unordered_map>

struct Key {
    std::size_t start_position;
    std::size_t remaining_num_batteries;

    [[nodiscard]] constexpr auto operator==(Key const&) const -> bool = default;
};

struct KeyHash {
    std::size_t operator()(const Key& k) const noexcept {
        std::size_t h1 = std::hash<std::size_t>{}(k.start_position);
        std::size_t h2 = std::hash<std::size_t>{}(k.remaining_num_batteries);
        return h1 ^ (h2 + 0x9e3779b97f4a7c15ull + (h1 << 6) + (h1 >> 2));
    }
};

struct KeyEqual {
    bool operator()(const Key& a, const Key& b) const noexcept {
        return a == b;
    }
};

auto cache = std::unordered_map<Key, std::size_t, KeyHash, KeyEqual>{};

[[nodiscard]] auto get_max_joltage(
    std::string const& bank,
    std::size_t const start_position,
    std::size_t const total_num_batteries,
    std::size_t const remaining_num_batteries
) -> std::size_t {
    auto const key = Key{
        .start_position = start_position,
        .remaining_num_batteries = remaining_num_batteries,
    };
    auto const find_it = cache.find(key);
    if (find_it != cache.cend()) {
        return find_it->second;
    }

    if (remaining_num_batteries == 1uz) {
        auto const result = std::ranges::max(
            std::views::transform(
                std::ranges::subrange(
                    bank.cbegin() + start_position,
                    bank.cend()
                ),
                [](char const c) { return c - '0'; }
            )
        );
        cache[key] = result;
        return result;
    }

    auto max_joltage = 0uz;
    for (auto const i : std::views::iota(start_position, bank.length() - (remaining_num_batteries - 1))) {
        auto const joltage =
            static_cast<std::size_t>(std::pow(10.0, remaining_num_batteries - 1uz)) * static_cast<std::size_t>(bank.at(i) - '0')
            + get_max_joltage(bank, i + 1, total_num_batteries, remaining_num_batteries - 1);
        max_joltage = std::max(max_joltage, joltage);
    }
    cache[key] = max_joltage;
    return max_joltage;
}

auto main(int const argc, char const * const * const argv) -> int {
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
        cache.clear();
        auto const joltage = get_max_joltage(line, 0uz, 12uz, 12uz);
        total += joltage;
    }

    std::cout << "total: " << total << '\n';
}
