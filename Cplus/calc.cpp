#include <iostream>
#include <optional>

// c++ reads code from top to bottom :-0
double addition(double x, double y) {
    return x + y; // returns an int (the sum value of x + y)
}

double subtration(double x, double y) {
    return x - y;
}

double multiplication(double x, double y) {
    return x * y;
}

std::optional<double> division(double x, double y) {
    if (y == 0) {
        return std::nullopt; // means return NO value
    } 
    return x / y; // else return a value
}

int main() { // expects an input as a return value
    double x;
    double y;
    char math_op;

    // prompt the user for x
    std::cout << "Give me x: ";
    std::cin >> x;

    // prompt the user for y
    std::cout << "Give me y: ";
    std::cin >> y;

    // prompt the for math_op
    std::cout << "What's the operation ? ";
    std::cin >> math_op;


    if (math_op == '+' ) {
        std::cout << "Performing addition of " << x <<  " + "  << y << " .... " << std::endl;
        double sum = addition(x, y);
        std::cout << "The sum of " << x << " + " << y << " is ... " << sum << std::endl;
    } else if (math_op == '-') {
        std::cout << "Performing subtration of " << x  << " - "  << y << std::endl;
        double subtract = subtration(x, y);
        std::cout << x << " - " << y << " = " << subtract << std::endl;
    } else if (math_op == '*') {
        std::cout << "Performing multiplication of " << x << " * " << y << std::endl;
        double multiply = multiplication(x, y);
        std::cout << x << " * " << y << " = " << multiply << std::endl;
    } else if (math_op == '/') {
        std::cout << "Performing division of " << x << " / " << y << " ...." << std::endl;
        std::optional<double> divide = division(x, y);
        if (divide.has_value()) { // if divide has a value...returns a bool, true if a value exists and false if a value DOESN'T exist
            std::cout << x << " / " << y << " = " << divide.value() << std::endl; // do the division of that value...divide.value() is like .unwrap() in rust, unwraps the actual value and the error and uses the value
        } else {
            std::cout << "WARNING: Cannot divide by zero" << std::endl;
        }
    } else {
        std::cout << "That's not a valid math operator :-( " << std::endl;
    }
    return 0; // cause said this main function requires an int as a return value
}
