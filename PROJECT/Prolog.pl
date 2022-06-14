/* ZMIENNE I WARUNKI */
% Комнаты (текущая позиция, описание позиции):
room(bedroom,
     ' Jesteś w swojej sypialni. Przed tobą są drzwi.').
room(corridor,
     ' Zostajesz w korytarzu. Nic specjalnego oprócz dziwnych dźwięków z łazienki.').
room(wardrobe,
     ' Jesteś w szafie.').
room(bathroom,
     ' Wszedłeś do łazienki ').
room(mainHallway, 
     ' Jesteś w głównym korytarzu. Nie dzieje się tu nic niezwykłego.').
room(diningRoom,
     ' Jesteś w jadalni. Nie dzieje się tu nic niezwykłego.').
room(livingRoom,
     ' Jesteś w salonie. Nie dzieje się tu nic niezwykłego.').
room(garden,
     ' Jesteś w ogrodzie, na zewnątrz domu.').


% Описания (комната, описание комнаты):
description(bedroom, 
            ' Rozglądasz się za czymś pożytecznym... Nic w tym pokoju Ci nie pomoże ').
description(corridor, 
            ' Została ci szafa. Przed tobą są drzwi do łazienki. W pobliżu znajdują się schody na parter. ').
description(wardrobe, 
            ' Znalazłeś leżący wallet kuchenny.').
description(mainHallway, 
            ' Nadal słychać te dźwięki dochodzące z piętra wyżej.
               Po lewej stronie widać jadalnię, a po prawej wyjście do ogrodu. W pobliżu są schody na parter').
description(diningRoom,
            ' Na środku pokoju widać duży stół jadalny. Jest na nim Twój telefon. Weź to i spróbuj do kogoś zadzwonić!').
description(livingRoom,
            'Nie ma tu nic pożytecznego.').


% ścieżka :
path(bedroom, corridor, north).
path(corridor, bedroom, south).
path(corridor, wardrobe, west).
path(wardrobe, corridor, east).
path(corridor, bathroom, north).
path(bathroom, corridor, south).
path(corridor, mainHallway, down).
path(mainHallway, corridor, up).
path(mainHallway, garden, east).
path(garden, mainHallway, west).
path(mainHallway, diningRoom, west).
path(diningRoom, mainHallway, east).
path(diningRoom, livingRoom, south).
path(livingRoom, diningRoom, north).



% Dynamic variables:(Zmienne)
:- dynamic position/2.
:- dynamic hasWallet/2.
:- dynamic hasPhone/2.
:- dynamic hasFullEq/2.


/* INWENTARZ */
inventory([wallet, phone]).%лист операций
showItems([First|Second]) :- write('Przedmioty: '), write(First), showItems(Second), nl.
showwallet([First|_]) :- write('Przedmioty: '), write(First), nl.
showPhone([_|Second]) :- write('Przedmioty: '), write(Second), nl. 

items :- % shows telephon
    position(you, CurrentPos),
    hasPhone(you, CurrentPos),
    inventory(Item), showPhone(Item).

items :- % shows portfel
    position(you, CurrentPos),
    hasWallet(you, CurrentPos),
    inventory(Item), showwallet(Item).

items :- % shows all items
    position(you, CurrentPos),
    hasFullEq(you, CurrentPos),
    inventory(Item), showItems(Item).

items :- 
    writeln('Nie masz żadnych przedmiotów.').


/* Ruch */

move(items) :-
    items.

move(take) :- % take portfel
    position(you, CurrentPos),
    wallet(CurrentPos).

move(pickup) :- % pickup telefon
    position(you, CurrentPos),
    phone(CurrentPos).
    
move(search) :- % показывает описание текущей позиции
    position(you, CurrentRoom), description(CurrentRoom, RoomDescription), writeln(RoomDescription).

move(Direction) :- % идет в определенном направлении
    position(you, CurrentPos),
    path(CurrentPos, NextPos, Direction),
    write('Ty idź '), write(Direction), write('...'),
    retract(position(you, CurrentPos)),
    assert(position(you, NextPos)),
    showPosition,
    !.   

move(_) :- % сообщение по умолчанию, когда была введена неверная команда
    writeln('Nie możesz tam iść. '),
    showPosition.


/* SITUATIONS */
escape :- % win 
    position(escape, CurrentPos),
    position(you, CurrentPos),
    writeln('Uciekłeś z tego nieznanego domu. Gratulacje!'), nl,
	retract(position(you, CurrentPos)),
	assert(position(you, gameOver)),
	!.
escape.

death :- % lose 
    position(death, CurrentPos),
    position(you, CurrentPos),
    writeln('zostałeś odkryty. Gra skończona.'), nl,
    retract(position(you, CurrentPos)),
    assert(position(you, gameOver)),
    !.
death.

wallet(CurrentPos) :- 
    position(wallet, CurrentPos),
    position(you, CurrentPos),
    retract(hasWallet(you, default)),
    assert(hasWallet(you, _)),
    writeln('Bierzesz portfel.'),
    !.

wallet(_) :- 
    writeln('Nie ma nic do zabrania!'),
    !.

phone(CurrentPos) :- 
    position(phone, CurrentPos),
    position(you, CurrentPos),
    retract(hasPhone(you, default)),
    assert(hasPhone(you, _)),
    writeln('Znalazłeś swój telefon.'),
    !.

phone(_) :- 
    writeln('Nie ma nic do odebrania!'),
    !.

hasWallet(you, default).
hasPhone(you, default).

        
/* TEXT na początku */
showControlls :- % показывает список доступных элементов управления
    nl,
    writeln('STEROWANIE:'),
    writeln('north, south, west, east, down, up, search, pickup, take, items').

showPosition :- % показывает текущую позицию
    nl, 
    position(you, CurrentPos), room(CurrentPos, PosDescription), writeln(PosDescription).



/* MAIN */
moveHandler :- % end 
    position(you, gameOver),
    writeln('Koniec!'),
    !.

moveHandler :- % основной цикл (główna pętla)
    nl,
    writeln('Ruszaj się'),
    read(Move),
    call(move(Move)),
    death,
    escape,
    moveHandler.

setGame :- % устанавливает позиции объектов
    retractall(position(_,_)),
    assert(position(you, bedroom)),
    assert(position(death, bathroom)),
    assert(position(wallet, wardrobe)),
    assert(position(phone, diningRoom)),
    assert(position(escape, garden)).

start :-
    setGame,
    writeln('New Game Started!'),
    showControlls,
    showPosition,
    moveHandler.