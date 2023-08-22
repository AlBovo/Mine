#include "colors.hpp"

#ifdef _WIN32
void print_with_color(char color){

    HANDLE hConsole = GetStdHandle(STD_OUTPUT_HANDLE);
    switch(color){
        case '1':
            SetConsoleTextAttribute(hConsole, BLUE);
            break;

        case '2':
            SetConsoleTextAttribute(hConsole, GREEN);
            break;
        
        case '3':
            SetConsoleTextAttribute(hConsole, RED);
            break;
        
        case '4':
            SetConsoleTextAttribute(hConsole, YELLOW);
            break;
        
        case '5':
            SetConsoleTextAttribute(hConsole, PURPLE);
            break;
        
        case '6':
            SetConsoleTextAttribute(hConsole, CYAN);
            break;
        
        case '7':
            SetConsoleTextAttribute(hConsole, MAGENTA);
            break;
        
        case '8':
            SetConsoleTextAttribute(hConsole, ORANGE);
            break;
        
        default:
            SetConsoleTextAttribute(hConsole, WHITE);
            break;
    }
    std::cout << color;
}
#endif

#ifdef __linux__

void print_with_color(char message){
    std::string ansi_string = "\033[";
    switch(message){
        case '0':
            ansi_string += strings::WHITE;
            break;
        case '1':
            ansi_string += strings::BLUE;
            break;

        case '2':
            ansi_string += strings::GREEN;
            break;
        
        case '3':
            ansi_string += strings::RED;
            break;
        
        case '4':
            ansi_string += strings::YELLOW;
            break;
        case '5':
            ansi_string += strings::PURPLE;
            break;
        
        case '6':
            ansi_string += strings::CYAN;
            break;
        
        case '7':
            ansi_string += strings::MAGENTA;
            break;
        
        case '8':
            ansi_string += strings::ORANGE;
            break;
        
        default:
            ansi_string += strings::DEFAULT;
            break;
    }
    ansi_string += "m" + std::string(1, message) + "\033[0m";
    std::cout << ansi_string;
}

#endif