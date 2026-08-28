#include <iostream>
#include <cstdlib> // required for std::getenv
#include <string>

int main() {
    // read the variable from the process env
    const char* env_val = std::getenv("GEMINI_API_KEY");

    if (env_val == nullptr) { // you can use !env_val..which still means the same thing
        std::cerr << "Error: GEMINI_API_KEY env var isn't set" << std::endl;
        return 1;
    }

    std::string gemini_api(env_val);
    std::cout << "GEMINI_API: " << gemini_api << std::endl;

    return 0;
}
