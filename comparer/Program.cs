using System;
using System.Linq;
using scheduleClass;

namespace comparer
{    
    internal class Program
    {
        static void Main(string[] args)
        {            
            Console.OutputEncoding = System.Text.Encoding.UTF8;            
            if (args.Length < 2)            
                throw new ArgumentException("Two arguments are required.");
            var output = new Schedule(args[0]) - new Schedule(args[1]);
            var fullNoChanges = new Schedule(output.header + string.Join("", Enumerable.Repeat("без змін\n", 44)));            
            Console.WriteLine((output == fullNoChanges) ? "без змін" : output);
        }
    }
}
