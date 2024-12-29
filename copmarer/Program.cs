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
            string header  { get; set; }
            string couple1 { get; set; }
            string couple2 { get; set; }
            string couple3 { get; set; }
            string couple4 { get; set; }
            string couple5 { get; set; }
            string couple6 { get; set; }
            string couple7 { get; set; }
        }        
        public string header { get; set; }
        public Day Monday    { get; set; }
        public Day Tuesday   { get; set; }
        public Day Wednesday { get; set; }
        public Day Thursday  { get; set; }        
        public Day Friday    { get; set; }
        public Day Saturday  { get; set; }
        public Day Sunday    { get; set; }

        public Scedule(string input)
        {
            string[] days = input.Split(new string[] { "-----" }, StringSplitOptions.RemoveEmptyEntries);
            header = days[0];
            Monday =    new Day("Понеділок",days[1],  days[2],  days[3],  days[4],  days[5],  days[6],  days[7]);
            Tuesday =   new Day("Вівторок", days[8],  days[9],  days[10], days[11], days[12], days[13], days[14]);
            Wednesday = new Day("Середа",   days[15], days[16], days[17], days[18], days[19], days[20], days[21]);
            Thursday =  new Day("Четвер",   days[22], days[23], days[24], days[25], days[26], days[27], days[28]);
            Friday =    new Day("Пятниця",  days[29], days[30], days[31], days[32], days[33], days[34], days[35]);
            Saturday =  new Day("Субота",   days[36], days[37], days[38], days[39], days[40], days[41], days[42]);
            Sunday =    new Day("Неділя",   days[43], days[44], days[45], days[46], days[47], days[48], days[49]);
        }
    }

    internal class Program
    {
        static void Main(string[] args)
        {
            string input = "-----Понеділок-----\r\n" +
                           "1 ПАРА: УРОЧИСТОСТІ З НАГОДИ ДНЯ ЗНАНЬ\r\n" +
                           "2 ПАРА: КУРАТОРСЬКА ГОДИНА\r\n" +
                           "3 ПАРА: нема\r\n" +
                           "4 ПАРА: нема\r\n" +
                           "5 ПАРА: нема\r\n" +
                           "6 ПАРА: нема\r\n" +
                           "7 ПАРА: нема\r\n" +
                           "-----Вівторок-----\r\n" +
                           "1 ПАРА: ВИЩА МАТЕМАТИКА (Лекція)\r\n" +
                           "2 ПАРА: МЕТОДИ ТА ЗАСОБИ КОМП'ЮТЕРНИХ ІНФОРМАЦІЙНИХ ТЕХНОЛОГІЙ (Лекція)\r\n" +
                           "3 ПАРА: ПРОГРАМУВАННЯ ТА АЛГОРИТМІЧНІ МОВИ (Лекція)\r\n" +
                           "4 ПАРА: нема\r\n" +
                           "5 ПАРА: нема\r\n" +
                           "6 ПАРА: нема\r\n" +
                           "7 ПАРА: нема\r\n" +
                           "-----Середа-----\r\n" +
                           "1 ПАРА: МЕТОДИ ТА ЗАСОБИ КОМП'ЮТЕРНИХ ІНФОРМАЦІЙНИХ ТЕХНОЛОГІЙ (Лекція)\r\n" +
                           "2 ПАРА: ДИСКРЕТНА МАТЕМАТИКА (Лекція)\r\n" +
                           "3 ПАРА: УКРАЇНСЬКА МОВА ЗА ПРОФЕСІЙНИМ СПРЯМУВАННЯМ (Лекція)\r\n" +
                           "4 ПАРА: нема\r\n" +
                           "5 ПАРА: нема\r\n" +
                           "6 ПАРА: нема\r\n" +
                           "7 ПАРА: нема\r\n" +
                           "-----Четвер-----\r\n" +
                           "1 ПАРА: нема\r\n" +
                           "2 ПАРА: ВИЩА МАТЕМАТИКА (Лекція)\r\n" +
                           "3 ПАРА: ПРОГРАМУВАННЯ ТА АЛГОРИТМІЧНІ МОВИ (Лекція)\r\n" +
                           "4 ПАРА: нема\r\n" +
                           "5 ПАРА: нема\r\n" +
                           "6 ПАРА: нема\r\n" +
                           "7 ПАРА: нема\r\n" +
                           "-----Пятниця-----\r\n" +
                           "1 ПАРА: ОЛІМПІЙСЬКИЙ УРОК\r\n" +
                           "2 ПАРА: ОЛІМПІЙСЬКИЙ УРОК\r\n" +
                           "3 ПАРА: нема\r\n" +
                           "4 ПАРА: нема\r\n" +
                           "5 ПАРА: нема\r\n" +
                           "6 ПАРА: нема\r\n" +
                           "7 ПАРА: нема\r\n" +
                           "-----Субота-----\r\n" +
                           "1 ПАРА: нема\r\n" +
                           "2 ПАРА: нема\r\n" +
                           "3 ПАРА: нема\r\n" +
                           "4 ПАРА: нема\r\n" +
                           "5 ПАРА: нема\r\n" +
                           "6 ПАРА: нема\r\n" +
                           "7 ПАРА: нема\r\n";
                           


        }
    }
}
