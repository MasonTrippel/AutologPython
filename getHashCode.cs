using System;

class Program
{
    static void Main(string[] args)
    {
        string input = args[0];
        int hashCode = input.GetHashCode();
        Console.WriteLine(hashCode);
    }
}