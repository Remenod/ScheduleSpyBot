using System;
using System.Collections;
using System.Collections.Generic;

namespace scheduleClass
{
    public class Schedule : IEnumerable<Schedule.Day>
    {
        public class Day : IEnumerable
        {
            public Day(string h, string c1, string c2, string c3, string c4, string c5, string c6, string c7)
            {
                header = h;
                couple1 = c1;
                couple2 = c2;
                couple3 = c3;
                couple4 = c4;
                couple5 = c5;
                couple6 = c6;
                couple7 = c7;
            }
            public Day()
            {
                header  = "Пара відсутня";
                couple1 = "Пара відсутня";
                couple2 = "Пара відсутня";
                couple3 = "Пара відсутня";
                couple4 = "Пара відсутня";
                couple5 = "Пара відсутня";
                couple6 = "Пара відсутня";
                couple7 = "Пара відсутня";
            }
            public string header { get; set; }
            public string couple1 { get; set; }
            public string couple2 { get; set; }
            public string couple3 { get; set; }
            public string couple4 { get; set; }
            public string couple5 { get; set; }
            public string couple6 { get; set; }
            public string couple7 { get; set; }
            public override string ToString()
            {
                return /*$"{header}\n" +*/
                       $"{couple1}\n" +
                       $"{couple2}\n" +
                       $"{couple3}\n" +
                       $"{couple4}\n" +
                       $"{couple5}\n" +
                       $"{couple6}\n" +
                       $"{couple7}";
            }
            public override bool Equals(object? obj) => obj is Day other && this == other;
            public override int GetHashCode() => base.GetHashCode();

            public bool isNoChanges() =>
                couple1 == "без змін" &&
                couple2 == "без змін" &&
                couple3 == "без змін" &&
                couple4 == "без змін" &&
                couple5 == "без змін" &&
                couple6 == "без змін" &&
                couple7 == "без змін";
            public IEnumerator GetEnumerator()
            {
                for (var i = 0; i < 6; i++)
                    yield return this[i];
            }

            public string this[int index]
            {
                get => index switch 
                    {
                        0 => couple1,
                        1 => couple2,
                        2 => couple3,
                        3 => couple4,
                        4 => couple5,
                        5 => couple6,
                        6 => couple7,
                        _ => throw new IndexOutOfRangeException("Індекс за межами діапазону.")
                    };                
                set
                {
                    switch (index) 
                    {
                        case 0:
                            couple1 = value;
                            break;
                        case 1:
                            couple2 = value;
                            break;
                        case 2:
                            couple3 = value;
                            break;
                        case 3:
                            couple4 = value;
                            break;
                        case 4:
                            couple5 = value;
                            break;
                        case 5:
                            couple6 = value;
                            break;
                        case 6:
                            couple7 = value;
                            break;
                        default:
                            throw new IndexOutOfRangeException("Індекс за межами діапазону.");
                    }
                }
            }

            public static Day operator -(Day a, Day b)
            {
                var (c1, c2, c3, c4, c5, c6, c7) = ("без змін", "без змін", "без змін", "без змін", "без змін", "без змін", "без змін");
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
            public static bool operator ==(Day a, Day b) =>
                 a.couple1 == b.couple1 &&
                 a.couple2 == b.couple2 &&
                 a.couple3 == b.couple3 &&
                 a.couple4 == b.couple4 &&
                 a.couple5 == b.couple5 &&
                 a.couple6 == b.couple6 &&
                 a.couple7 == b.couple7;
            public static bool operator !=(Day a, Day b) => !(a == b);
        }
        public string header { get; set; }
        public Day Monday { get; set; }
        public Day Tuesday { get; set; }
        public Day Wednesday { get; set; }
        public Day Thursday { get; set; }
        public Day Friday { get; set; }
        public Day Saturday { get; set; }

        public Schedule(string input)
        {
            var inputSplitted = input.Split("\n");
            if (inputSplitted.Length >= 43)
            {
                string[] data = new string[43];
                Array.Fill(data, "Пара відсутня");
                Array.Copy(inputSplitted, data, 43);
                header    = data[0];
                Monday    = new Day("Понеділок", data[1],  data[2],  data[3],  data[4],  data[5],  data[6],  data[7]);
                Tuesday   = new Day("Вівторок",  data[8],  data[9],  data[10], data[11], data[12], data[13], data[14]);
                Wednesday = new Day("Середа",    data[15], data[16], data[17], data[18], data[19], data[20], data[21]);
                Thursday  = new Day("Четвер",    data[22], data[23], data[24], data[25], data[26], data[27], data[28]);
                Friday    = new Day("Пятниця",   data[29], data[30], data[31], data[32], data[33], data[34], data[35]);
                Saturday  = new Day("Субота",    data[36], data[37], data[38], data[39], data[40], data[41], data[42]);
            }
            else if (inputSplitted.Length == 1)
            {
                header    = inputSplitted[0];
                Monday    = new Day();
                Tuesday   = new Day();
                Wednesday = new Day();
                Thursday  = new Day();
                Friday    = new Day();
                Saturday  = new Day();
            }
            else throw new Exception("Invalid input");
        }
        public static Schedule operator -(Schedule a, Schedule b) =>        
            new Schedule($"зміни в {a.header} відносно {b.header}")
            {
                Monday    = a.Monday    - b.Monday,
                Tuesday   = a.Tuesday   - b.Tuesday,
                Wednesday = a.Wednesday - b.Wednesday,
                Thursday  = a.Thursday  - b.Thursday,
                Friday    = a.Friday    - b.Friday,
                Saturday  = a.Saturday  - b.Saturday
            };        
        public static bool operator ==(Schedule a, Schedule b) =>
             a.Monday    == b.Monday &&
             a.Tuesday   == b.Tuesday &&
             a.Wednesday == b.Wednesday &&
             a.Thursday  == b.Thursday &&
             a.Friday    == b.Friday &&
             a.Saturday  == b.Saturday;
        public static bool operator !=(Schedule a, Schedule b) => !(a == b);
        public override bool Equals(object? obj) => obj is Schedule other && this == other;
        public override int GetHashCode() => base.GetHashCode();
        public override string ToString()
        {
            return /*$"{header   }\n" +*/
                   $"{Monday}\n" +
                   $"{Tuesday}\n" +
                   $"{Wednesday}\n" +
                   $"{Thursday}\n" +
                   $"{Friday}\n" +
                   $"{Saturday}\n";
        }
        public Day this[int index] 
        {
            get => index switch
                {
                    0 => Monday,
                    1 => Tuesday,
                    2 => Wednesday,
                    3 => Thursday,
                    4 => Friday,
                    5 => Saturday,
                    _ => throw new IndexOutOfRangeException("Індекс за межами діапазону.")
                };
            set 
            {
                switch (index)
                {
                    case 0:
                        Monday = value;
                        break;
                    case 1:
                        Tuesday = value;
                        break;
                    case 2:
                        Wednesday = value;
                        break;
                    case 3:
                        Thursday = value;
                        break;
                    case 4:
                        Friday = value;
                        break;
                    case 5:
                        Saturday = value;
                        break;
                    default:
                        throw new IndexOutOfRangeException("Індекс за межами діапазону.");
                }
            }
        }
        public IEnumerator<Day> GetEnumerator()
        {
            for (var i = 0; i < 6; i++)
                yield return this[i];
        }

        IEnumerator IEnumerable.GetEnumerator()
        {
            throw new NotImplementedException();
        }
    }
}
