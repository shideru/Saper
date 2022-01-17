# vowpal wabbit - podprojekt indywidualny, Marek Gulawski

## Generowanie modelu decyzyjnego dla sapera

<p>Do wygenerowania modedlu decyzyjnego wykorzystywanego przex vowpal wabbit służy "wabbit_generator.py".
Program przechodzi mapy zapisane w folderze maps wykorzystując wybrany algorytm, w tym przypadku algorytm A*.
Każdy wykonany ruch oraz otoczenie sapera jest wpisywane dopisywane do pliku "wabbit_examples" w nowej linii w postaci która jest przeznaczona do odczytu przez vowpal wabbit.</p>

<p>Format zapisu jest następujący:
[ruch] | [1x1]:.[obiekt] [1x2]:.[objekt] ... [5x5]:.[obiekt]
Gdzie:
<ol>
<li>[ruch] - Tutaj ruchom w prawo, dół, lewo, górę odpowiadają cyfry, odpowiednio '1', '2', '3', '4'</li>
<li>[1x1] - itd. odpowiada indeksą otoczenia wokół sapera. składa się z liczb od 1 do 5 oprócz indeksu [3x3] który odpowiada saperowi</li>
<li>[objekt] - symbolicznie oznacza obiekty na mapie. '0' odpowiada współrzędnej poza mapą, '5' ospowiada rozbrojonej bąbie, '10' odpowiada pustej przestrzeni, '50' odpowiada nierozbrojonej bąbie</li>
</ol>
</p>

<p>Program wykonuje mapy z folderu 'maps' ustaloną ilość razy. Liczbę tę można edytować aby generować mniej lub więcej przykładów ruchu do uczenia. Po tej części wykonywana jest komenda tworząca model decyzyjny na podstawie pliku "wabbit_examples". Plik jest w formacie który vowpal wabbit używa do poruszania saperem.</p>

## Przechodzenie mapy przy pomocy vowpal wabbit
<p>Do przyechodzenia po mapie służy "vw_saper.py", pokazując ruchy w środowisku pygame. W pętli wykonuje operacje poruszania się po mapie. Najpierw zapisuje on swoje własne położenie i otoczenie w podobnym formacie jak wyżej ale bez wartości ruch. Następnie program wykonuje komende zwracającą przewidziany ruch dla danego otoczenia. W przypadku gdy przewidziany ruch jest taki sam 21 razy z rzędu a saper nie zmienił otoczenia jest on przesówany w losowe miejsce aby kontynuować z innego otoczenia.</p>