# Sztuczna Inteligencja Projekt

Grupa projektowa:
Zofia Bączyk
Marek Gulawski
Witold Borowiak

Temat: Automatyczny saper


Decision classification and regression tree.
<p>training_data to array złożona z trzech kolorów kabli A, B, C oraz cut czyli kabla do przecięcia.
możliwe kolory to: Red, Green, Blue, Yellow</p>
przykład: ['Red', 'Green', 'Blue', 'Red']
<p>Pytania wybierane są przez najlepszy przyrost informacji i dzielone są na gałęzie true i false, dane w nich są klasyfikowane przez ilość możliwości, drzewo kończy się kiedy nie mamy więcej pytań do zadania.</p>
<p>Program tworzy drzewo decyzyjne na podstawie "training_data" dla przykładowych danych:</p>

![image](https://drive.google.com/uc?export=viev&id=172unlJo4eQp4FafSsivmy-0QQWiXfTvJ)
<p>Podany dataset nie tworzy rzadnych niepewności, czyli nie posiada żadnych nieodróżnialnych zestawów danych o różnych wynikach. </p>
<p>Każda bomba dostaje randomowo przyporządkowaną kombinację kabli A, B, C oraz jaki kolor należy przeciąć.
Program wykonuje funkcję classify dla wylosowanej kombinacji i wygenerowanego drzewa decyzyjnego.
Po przejściu drzewa i znalezieniu się w liściu zwracana jest lista kolorów.
Program wyświetla w konsoli nazwę wylosowanego koloru i koloru wybranego przez drzewo.
Bomba wyświetla przecięty kolor (wybór drzewa) oraz prawidłowy kolor w dolnym jego narożniku.</p>

![image](https://drive.google.com/uc?export=viev&id=1xhcGOL14NPAdcNwpM1Wpd2fgQvnZhKm5)

vs_saper_zb.py

wykorzystano google developer tutorials


