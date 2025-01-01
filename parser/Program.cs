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
                            var before = day[i].Split("->")[0].Split("$[]");
                            var after   = day[i].Split("->")[1].Split("$[]");
                            if (before.Length > 1)                             
                                output += $"Було:\n```\n{before[0]}\n{before[1]}\n```";
                            else
                                output += $"Було:\n```\n{before[0]}\n```";
                            if (after.Length > 1)
                                output += $"Стало:\n```\n{after[0]}\n{after[1]}\n```";
                            else
                                output += $"Стало:\n```\n{after[0]}\n```";
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
