Globalnie tworzona jest lista [Solutions], do ktorej wpisywane są ścieżki znalezione przez funkcje [bfs_find].

Funkcja [bfs_find] przyjmuje argumenty:
- [Grid] - mapa
- [start] - współżędne początkowe
- [dest] - współrzędne bomb na mapie (lista)

Działanie funkcji [bfs_find]:
1. Na początku tworzone są listy [Closed_set], [Open_set], [cameFrom], [Grid2]:
	- [Closed_set] - lista zawierająca współrzędne sprawdzonych punktów
	- [Open_set] - lista zawierająca współrzędne punktów do odwiedzenia (z początkową wartością [start])
	- [cameFrom] - po wykonaniu algorytmu w tej liście będzie zachowana ścieżka od znalezionej bomby do startu
	- [Grid2] - pomocnicza lista zawierająca kopie mapy z zamienionymi nieodwiedzonymi bombami (z listy dest) na ściany
2. tworzona jest zmienna [flag3] przechowująca wartość True służca do zatrzymania pętli po wyszukaniu ścieżki
3. Wykonanie w pętli kroków: 4,5,6,7,8 aż nie skończą się współrzędne na liście [Open_set] lub flag3 będzie przechowywać False
	4. Przypisanie współrzędnych pod pierwszym indeksem na liście [Open_set] do listy [current]
	5. Sprawdzenie czy [current] jest jedną z współrzędnych na liście [dest]
		Jeżeli jest, ich indeks na lisćie [dest] jest zapisywany w zmiennej goal, zmienna flag3 przyjmuje wartość False oraz pętla jest pomijana
	6. Usunięcie współrzędnych na pierwszym indeksie listy [Open_set]
	7. Dodanie tych współrzędnych do listy [Closed_set]
	8. Sprawdzenie sąsiadów współrzędnych przypisanych [current] różnych od ściany:
	Jeżeli nie ma ich na liście [Closed_set] są dopisywane do listy [Open_set] oraz na ich współrzędne na liście [cameFrom] wpisywane są współrzędne z [current]
9. Zapisanie ścieżki w postaci współrzędnych z [cameFrom] do listy [Path]
10. Zamiana współrzędnych na listę kroków w postaci ['R', 'L', 'U', 'D'] gdzie R - prawo, L - lewo, - U - góra, D - dół
11. Usunięcie współrzędnych znalezionej bomby z listy [dest]
12. Jeżeli lista [dest] nie jest pusta wywołuje się algorytm [bfs_find] ze zmienionymi argumentami 
([Grid], [współrzędne przed znalezioną bombą], [dest])
	