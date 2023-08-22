#ifndef COLORS_HPP
#define COLORS_HPP
#include <iostream>

void print_with_color(char message);

#ifdef _WIN32
#include <windows.h>

enum { //TODO: test on windows
    BLACK             = 0,
    DARKBLUE          = FOREGROUND_BLUE,
    DARKGREEN         = FOREGROUND_GREEN,
    DARKCYAN          = FOREGROUND_GREEN | FOREGROUND_BLUE,
    DARKRED           = FOREGROUND_RED,
    DARKMAGENTA       = FOREGROUND_RED | FOREGROUND_BLUE,
    DARKYELLOW        = FOREGROUND_RED | FOREGROUND_GREEN,
    DARKGRAY          = FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE,
    GRAY              = FOREGROUND_INTENSITY,
    PURPLE            = FOREGROUND_INTENSITY | FOREGROUND_RED | FOREGROUND_BLUE,
    ORANGE            = FOREGROUND_INTENSITY | FOREGROUND_RED | FOREGROUND_GREEN,
    BLUE              = FOREGROUND_INTENSITY | FOREGROUND_BLUE,
    GREEN             = FOREGROUND_INTENSITY | FOREGROUND_GREEN,
    CYAN              = FOREGROUND_INTENSITY | FOREGROUND_GREEN | FOREGROUND_BLUE,
    RED               = FOREGROUND_INTENSITY | FOREGROUND_RED,
    MAGENTA           = FOREGROUND_INTENSITY | FOREGROUND_RED | FOREGROUND_BLUE,
    YELLOW            = FOREGROUND_INTENSITY | FOREGROUND_RED | FOREGROUND_GREEN,
    WHITE             = FOREGROUND_INTENSITY | FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE,
};
#endif
#ifdef __linux__

namespace strings{
    const std::string RED = "38;2;255;0;0";
    const std::string GREEN = "38;2;0;255;0";
    const std::string YELLOW = "38;2;255;255;0";
    const std::string BLUE = "38;2;0;0;255";
    const std::string MAGENTA = "38;2;255;0;255";
    const std::string CYAN = "38;2;0;255;255";
    const std::string WHITE = "38;2;255;255;255";
    const std::string PURPLE = "38;2;146;231;255";
    const std::string ORANGE = "38;2;255;127;80";
    const std::string DEFAULT = "49";
};

#endif
#endif