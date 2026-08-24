extern "C" { // this tells the C++, to keep this fn clean (don't mangle it) so other langs can find it
    int add_numbers(int a, int b) {
        return a + b;
    }
}
