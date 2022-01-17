# Autonomiczny saper. Projekt SI część druga etap wspólny

## Heurystyka
<p>heuristic_function_cost - funkcja która oblicza odległość między dwoma punktami według normy manhattan: (różnica x-ów + różnica y-ów).

## Algorytm planowania trasy
<p>A_star_pf - [linie kodu 59-163] wyznacza ścierzkę pomiędzy pozycją sapera a bombą o najwyższym pryjorytecie która nie została jeszcze rozborjona. 
Robi op poprzez stworzenie tablicy dwuwymiarowej, której elementy odpowiadają polom planszy a ich wartości 
podpowiadają kosztowy przemieszczenia się do nich z pola sapera obliczonym według funkcji heuristic_function_cost.
Następnie saper udaje się do bomby i rozbraja ją,po czym algorytm a* wyznacza tą samą metodą drogę do nasępnej bomby
o ile jeszcze jakaś nie jest rozborjona.

![image](https://drive.google.com/uc?export=view&id=12841Ld_ol1D65wpiqUmKsnMpSVIVC4EO)
