using System;
using scheduleClass;

namespace parser
{    

    internal class Program
    {
        static string ParseChanges(string data)
        {
            var schedule = new Scedule("\n"+data);            
            var output = "";
            foreach (var day in schedule)
                if (!day.isNoChanges())
                {
                    output += "\n*" + day.header.ToUpper() + "*\n";
                    for (var i = 0; i < 7; i++)
                        if (day[i] != "без змін")
                        {
                            output += $"_ПАРА {i + 1}:_\n";
                            output += $"Було:\n```\n{day[i].Split("->")[0]}\n```";
                            output += $"Стало:\n```\n{day[i].Split("->")[1]}\n```";                            
                        }
                }

            return output;
        }
        static void Main(string[] arg)
        {
            Console.OutputEncoding = System.Text.Encoding.UTF8;
            Console.WriteLine(ParseChanges(arg[0]));
        }
    }
}
