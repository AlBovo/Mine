#include "utils.hpp"

player::player(std::string name) : dist(0, SIZE-1){
    this->name = name;
    std::random_device rd;
    this->rng = std::mt19937(rd());
}

/*      GENERATOR OF THE MATRIX     */
void player::generator(int x_p, int y_p){ // first choice of the player
    std::array<std::pair<int, int>, NUMBER_OF_MINES> mines;
    this->matrix[x_p][y_p] = -1;

    for(int i = 0; i < NUMBER_OF_MINES; i++){
        int x, y;
        do{
            
            x = dist(rng);
            y = dist(rng);
        }while(this->matrix[x][y] == -1);

        this->matrix[x][y] = -1;
        mines[i] = {x, y};
    }

    this->matrix[x_p][y_p] = 0;
    
    for(auto &i : mines){        
        if(i.first > 0 && matrix[i.first-1][i.second] != -1)
            matrix[i.first-1][i.second]++;
        if(i.first < SIZE-1 && matrix[i.first+1][i.second] != -1)
            matrix[i.first+1][i.second]++;
        if(i.second > 0 && matrix[i.first][i.second-1] != -1)
            matrix[i.first][i.second-1]++;
        if(i.second < SIZE-1 && matrix[i.first][i.second+1] != -1)
            matrix[i.first][i.second+1]++;

        if(i.first > 0 && i.second > 0 && matrix[i.first-1][i.second-1] != -1)
            matrix[i.first-1][i.second-1]++;
        if(i.first > 0 && i.second < SIZE-1 && matrix[i.first-1][i.second+1] != -1)
            matrix[i.first-1][i.second+1]++;
        if(i.first < SIZE-1 && i.second > 0 && matrix[i.first+1][i.second-1] != -1)
            matrix[i.first+1][i.second-1]++;
        if(i.first < SIZE-1 && i.second < SIZE-1 && matrix[i.first+1][i.second+1] != -1)
            matrix[i.first+1][i.second+1]++;
    }
}
/*      END GENERATOR OF THE MATRIX     */

/*      PRINT MATRIX FUNCTION       */
void player::print_matrix(){
    for(int i = 0; i < SIZE; i++){
        for(int e = 0; e < SIZE; e++){
            if(this->discovered[i][e])
                std::cout << this->matrix[i][e] << " ";
            else
                std::cout << "X ";
        }
        std::cout << std::endl;
    }
}
/*      END PRINT MATRIX FUNCTION       */

/*      DISCOVER IF EMPTY FUNCTION      */
void player::discover_if_empty(int x, int y){
    if(this->discovered[x][y])
        return;
    if(this->matrix[x][y] == 0){
        discovered_number++;
        this->discovered[x][y] = 1;
        if(x > 0)
            discover_if_empty(x-1, y);
        if(x < SIZE-1)
            discover_if_empty(x+1, y);
        if(y > 0)
            discover_if_empty(x, y-1);
        if(y < SIZE-1)
            discover_if_empty(x, y+1);
        
        if(x > 0 && y > 0)
            discover_if_empty(x-1, y-1);
        if(x > 0 && y < SIZE-1)
            discover_if_empty(x-1, y+1);
        if(x < SIZE-1 && y > 0)
            discover_if_empty(x+1, y-1);
        if(x < SIZE-1 && y < SIZE-1)
            discover_if_empty(x+1, y+1);
    }
    else if(this->matrix[x][y] > 0){
        this->discovered[x][y] = 1;
        discovered_number++;
    }
}
/*      END DISCOVER IF EMPTY FUNCTION      */

/*      INIZIALIZE MATRIX FUNCTION     */
void player::initalize_matrix(){
    for(int i = 0; i < SIZE; i++){
        for(int e = 0; e < SIZE; e++){
            this->matrix[i][e] = 0;
            this->discovered[i][e] = 0;
        }
    }
}
/*      END INIZIALIZE MATRIX FUNCTION     */

/*      GAME FUNCTION     */
void player::start_game(){
    int discovered_number = 0;
    // Initizalize matrix and discovered with 0
    this->initalize_matrix();

    while(discovered_number < (SIZE*SIZE)-NUMBER_OF_MINES){
        int x = -1, y = -1;
        std::string x_buffer, y_buffer;
        
        this->print_matrix();

        while(x < 0 || x > SIZE-1 || y < 0 || y > SIZE-1){
            std::cout << "Enter the coordinates: ";
            std::cin >> x_buffer >> y_buffer;

            if(x_buffer.length() > 2 || y_buffer.length() > 2){
                std::cout << "Invalid coordinates" << std::endl;
                continue;
            }
            
            try{
                y = std::stoi(x_buffer) - 1;
                x = std::stoi(y_buffer) - 1;
            } catch(std::invalid_argument){
                std::cout << "Invalid coordinates" << std::endl;
                continue;
            }
            
            if(discovered[x][y]){
                std::cout << "You already discovered this coordinate" << std::endl;
                x = y = -1;
                continue;
            }

            if(x < 0 || x > SIZE-1 || y < 0 || y > SIZE-1){
                std::cout << "Invalid coordinates" << std::endl;
            }
        }
        if(discovered_number == 0)
            this->generator(x, y);

        if(this->matrix[x][y] == -1){
            std::cout << "[+] ***** You lost! ****** [+]" << std::endl;
            break;
        }

        if(this->matrix[x][y] == 0){
            this->discover_if_empty(x, y);
        }
        else{
            this->discovered[x][y] = 1;
            discovered_number++;
        }
    }
    
    this->print_matrix();

    if(discovered_number == (SIZE*SIZE)-NUMBER_OF_MINES)
        std::cout << "[+] ***** You won! ****** [+]" << std::endl;
}
/*      END START THE GAME FUNCTION     */