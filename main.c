#include <stdio.h>
#include <stdlib.h>

int main(int argc, char const *argv[])
{
    char command[] = ".\\.venv\\Scripts\\python.exe .\\src\\main.py";
    printf("%s\n", command);
    system(command);
    system("pause");
    return 0;
}
