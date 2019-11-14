#include<iostream>
using namespace std;

int main()
{
    int a = 1;
    int b = 2;
    for (int i = 0; i < 10 ; i++)
    {
        a += b;
    }
    cout << a << endl;
    return 0;
}