#include<stdio.h>

int main()
{
    int first = 10;
    int second = 12;
    int i = 0;
    while(i != 10)
    {
        first += second;
        i++;
    }
    printf("%d",first);
    return 0;
}