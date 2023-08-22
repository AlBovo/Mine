#ifndef UTILS_HPP
#define UTILS_HPP

#define SIZE 16 // TODO: Implement other sizes
#define NUMBER_OF_MINES (SIZE * SIZE) / 8 // one bomb every 8 cells

#include <string>
#include <iostream>
#include <utility>
#include <assert.h>
#include <array>

class player{
private:
    std::string name; // name of the player
    int discovered_number; // number of discovered cells
    int matrix[SIZE][SIZE]; // matrix of the game
    bool discovered[SIZE][SIZE]; // matrix of discovered cells

    void generator();
    void discover_if_empty(int x, int y);

public:
    player(std::string name);
    void print_matrix();
    void start_game();
};

const std::string options[] = {
    "1. Start a new game",
    "2. Show scoreboard",
    "3. Exit"
};

#endif