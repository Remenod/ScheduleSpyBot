using System;

namespace copmarer
{

    public class Scedule 
    {
        public class Day
        {
            public Day(string h, string c1, string c2, string c3, string c4, string c5, string c6, string c7)
            {
                couple1 = c1;
                couple2 = c2;
                couple3 = c3;
                couple4 = c4;
                couple5 = c5;
                couple6 = c6;
                couple7 = c7;
            }
            string header { get; set; }
            string couple1 { get; set; }
            string couple2 { get; set; }
            string couple3 { get; set; }
            string couple4 { get; set; }
            string couple5 { get; set; }
            string couple6 { get; set; }
            string couple7 { get; set; }
            public override string ToString()
            {
                return $"{header}\n" +
                       $"{couple1}\n" +
                       $"{couple2}\n" +
                       $"{couple3}\n" +
                       $"{couple4}\n" +
                       $"{couple5}\n" +
                       $"{couple6}\n" +
                       $"{couple7}";
            }
            public static Day operator -(Day a, Day b) 
            {
                var (c1,c2,c3,c4,c5,c6,c7) = ("","","","","","","");                
                if (a.header != b.header)                
                    throw new Exception("Different days");

                if (a.couple1 != b.couple1)
                    c1 = $"{a.couple1}->{b.couple2}";

                if (a.couple2 != b.couple2)
                    c2 = $"{a.couple2}->{b.couple2}";

                if (a.couple3 != b.couple3)                                    
                    c3 = $"{a.couple3}->{b.couple3}";

                if (a.couple4 != b.couple4)
                    c4 = $"{a.couple4}->{b.couple4}";

                if (a.couple5 != b.couple5)
                    c5 = $"{a.couple5}->{b.couple5}";

                if (a.couple6 != b.couple6)
                    c6 = $"{a.couple6}->{b.couple6}";

                if (a.couple7 != b.couple7)
                    c7 = $"{a.couple7}->{b.couple7}";

                return new Day(a.header, c1, c2, c3, c4, c5, c6, c7);
            }
        }        
        public string header { get; set; }
        public Day Monday    { get; set; }
        public Day Tuesday   { get; set; }
        public Day Wednesday { get; set; }
        public Day Thursday  { get; set; }        
        public Day Friday    { get; set; }
        public Day Saturday  { get; set; }

        public Scedule(string input)
        {
            var inputSplitted = input.Split("\n");            
            if (inputSplitted.Length == 43) 
            {                 
                string[] data = new string[43];
                Array.Fill(data, "нема");
                Array.Copy(inputSplitted, data, 43);
                header    = data[0];
                Monday    = new Day("Понеділок", data[1],  data[2],  data[3],  data[4],  data[5],  data[6],  data[7]);
                Tuesday   = new Day("Вівторок" , data[8],  data[9],  data[10], data[11], data[12], data[13], data[14]);
                Wednesday = new Day("Середа"   , data[15], data[16], data[17], data[18], data[19], data[20], data[21]);
                Thursday  = new Day("Четвер"   , data[22], data[23], data[24], data[25], data[26], data[27], data[28]);
                Friday    = new Day("Пятниця"  , data[29], data[30], data[31], data[32], data[33], data[34], data[35]);
                Saturday  = new Day("Субота"   , data[36], data[37], data[38], data[39], data[40], data[41], data[42]);     
            }
            else if (inputSplitted.Length == 1)
                header = inputSplitted[0];
            else throw new Exception("Invalid input");
        }
        public static Scedule operator -(Scedule a, Scedule b) 
        {
            return new Scedule($"зміни в {a.header} відносно {b.header}")
            {
                Monday    = a.Monday    - b.Monday,
                Tuesday   = a.Tuesday   - b.Tuesday,
                Wednesday = a.Wednesday - b.Wednesday,
                Thursday  = a.Thursday  - b.Thursday,
                Friday    = a.Friday    - b.Friday,
                Saturday  = a.Saturday  - b.Saturday
            };
        }
        public override string ToString()
        {
            return $"{header   }\n" +
                   $"{Monday   }\n" +
                   $"{Tuesday  }\n" +
                   $"{Wednesday}\n" +
                   $"{Thursday }\n" +
                   $"{Friday   }\n" +
                   $"{Saturday }\n";
        }
    }

    internal class Program
    {
        static void Main(string[] args)
        {
            Console.OutputEncoding = System.Text.Encoding.Unicode;
            string input = "4т (23.09-28.09.2024)\nнема\nВИЩА МАТЕМАТИКА (Лекція)\nДИСКРЕТНА МАТЕМАТИКА (Лекція)\nПРОГРАМУВАННЯ ТА АЛГОРИТМІЧНІ МОВИ (Лекція)\nФІЗИЧНА КУЛЬТУРА\nнема\nнема\nМЕТОДИ ТА ЗАСОБИ КОМП'ЮТЕРНИХ ІНФОРМАЦІЙНИХ ТЕХНОЛОГІЙ (Лекція)\nПРОГРАМУВАННЯ ТА АЛГОРИТМІЧНІ МОВИ (Лекція)\nТЕАТРАЛЬНА КУЛЬТУРА УКРАЇНИ Й ЗАХІДНОЇ ЄВРОПИ (Лекція)\nКУЛЬТУРА НАУКОВО-ДОСЛІДНИЦЬКОЇ КОМПЕТЕНТНОСТІ ФАХІВЦЯ (Лекція) / ТЕАТРАЛЬНА КУЛЬТУРА УКРАЇНИ Й ЗАХІДНОЇ ЄВРОПИ (Лекція) / ІСТОРІЯ УКРАЇНСЬКОЇ КУЛЬТУРИ (Лекція)\nФІЗИЧНА КУЛЬТУРА\nнема\nнема\nнема\nнема\nУКРАЇНСЬКА МОВА ЗА ПРОФЕСІЙНИМ СПРЯМУВАННЯМ (Пр)\nКУЛЬТУРА НАУКОВО-ДОСЛІДНИЦЬКОЇ КОМПЕТЕНТНОСТІ ФАХІВЦЯ (Лекція)\nнема\nнема\nнема\nМТЗКІТ(Л.р.)\nДискретна математика (Практика)\nПАЛМ (Л.р.)\nІноземна мова (Пр)\nнема\nнема\nнема\nнема\nВища математика (Практика)\nЕКСКУРСІЯ ДО МУЗЕЮ НАУКОВОЇ БІБЛІОТЕКИ\nнема\nнема\nнема\nнема\nнема\nІСТОРІЯ УКРАЇНСЬКОЇ КУЛЬТУРИ (Лекція)\nІСТОРІЯ УКРАЇНСЬКОЇ КУЛЬТУРИ (Лекція)\nнема\nнема\nнема\nнема";
            string input2 = "5т (30.09-05.10.2024)\nнема\nВИЩА МАТЕМАТИКА (Лекція)\nДИСКРЕТНА МАТЕМАТИКА (Лекція)\nПРОГРАМУВАННЯ ТА АЛГОРИТМІЧНІ МОВИ (Лекція)\nФІЗИЧНА КУЛЬТУРА\nнема\nнема\nнема\nПРОГРАМУВАННЯ ТА АЛГОРИТМІЧНІ МОВИ (Лекція)\nТЕАТРАЛЬНА КУЛЬТУРА УКРАЇНИ Й ЗАХІДНОЇ ЄВРОПИ (Лекція)\nКУЛЬТУРА НАУКОВО-ДОСЛІДНИЦЬКОЇ КОМПЕТЕНТНОСТІ ФАХІВЦЯ (Лекція) / ТЕАТРАЛЬНА КУЛЬТУРА УКРАЇНИ Й ЗАХІДНОЇ ЄВРОПИ (Лекція)\nФІЗИЧНА КУЛЬТУРА\nнема\nнема\nнема\nнема\nУКРАЇНСЬКА МОВА ЗА ПРОФЕСІЙНИМ СПРЯМУВАННЯМ (Пр)\nКУЛЬТУРА НАУКОВО-ДОСЛІДНИЦЬКОЇ КОМПЕТЕНТНОСТІ ФАХІВЦЯ (Лекція)\nФІЗИЧНА КУЛЬТУРА\nнема\nнема\nМТЗКІТ(Л.р.)\nДискретна математика (Практика)\nПАЛМ (Л.р.)\nІноземна мова (Пр)\nОформлення банківських карток\nнема\nнема\nнема\nВища математика (Практика)\nнема\nнема\nнема\nнема\nнема\nнема\nІСТОРІЯ УКРАЇНСЬКОЇ КУЛЬТУРИ (Лекція)\nІСТОРІЯ УКРАЇНСЬКОЇ КУЛЬТУРИ (Лекція)\nнема\nнема\nнема\nнема";
            Scedule scedule = new Scedule(input);
            Scedule scedule2 = new Scedule(input2);
            Console.WriteLine(scedule-scedule2);



        }
    }
}
