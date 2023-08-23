#include <iostream>
#include <ctime>
#include "utils.hpp"

int main(){
    std::string name, decision;

    std::cout << "Enter your name: ";
    std::cin >> name;
    player player(name);

    do{
        for(auto &i : options){
            std::cout << i << std::endl;
        }
        std::cin >> decision;

        if(decision.length() > 1){
            std::cout << "Invalid option" << std::endl;
            continue;
        }

        switch(decision[0]){
            case '1':
                std::cout << "Starting a new game..." << std::endl;
                player.start_game();
                break;
            case '2':
                std::cout << "Showing scoreboard..." << std::endl; // TODO: Implement scoardboard
                break;
            case '3':
                std::cout << "Exiting..." << std::endl;
                break;
            default:
                std::cout << "Invalid option" << std::endl;
                break;
        }
    }while(decision[0] != '3');
    return 0;
}