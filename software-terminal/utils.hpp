#ifndef UTILS_HPP
#define UTILS_HPP

#define SIZE 16 // TODO: Implement other sizes
#define NUMBER_OF_MINES (SIZE * SIZE) / 8 // one bomb every 8 cells

#include <string>
#include <iostream>
#include <utility>
#include <assert.h>
#include <array>
#include <random>

#include "colors.hpp"

class player{
private:
    std::string name; // name of the player
    int discovered_number; // number of discovered cells
    std::mt19937 rng; // random number generator
    std::array<std::array<int, SIZE>, SIZE> matrix; // matrix of the game
    std::array<std::array<int, SIZE>, SIZE> discovered; // matrix of discovered cells
    std::uniform_int_distribution<> dist; // distribution of the random number generator

    void initalize_matrix();
    void generator(int x, int y);
    void discover_if_empty(int x, int y);

public:
    player(std::string name);
    void print_matrix(bool lost);
    void start_game();
};

const std::string options[] = {
    "1. Start a new game",
    "2. Show scoreboard",
    "3. Exit"
};

#endif