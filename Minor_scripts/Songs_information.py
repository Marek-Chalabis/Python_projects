# coding=utf8

'''
program will format text from wikipedia about songs (in this example first album by queen - https://pl.wikipedia.org/wiki/Queen_(album)) nad show inf. for the specific song),
and will return information about specific one
'''


DISC = 'Queen (album)'
ALBUM = '''
Keep Yourself Alive
Brian May napisał „Keep Yourself Alive” już po powstaniu zespołu, ale zanim dołączył do niego John Deacon, jak potwierdził basista Barry Mitchell. Zgodnie z tym, co May powiedział w radiu na temat albumu z 1977, News of the World, gdy napisał ten utwór chciał, aby był odebrany jako żartobliwy i ironiczny, lecz sens zmienił się kompletnie, gdy śpiewał go Freddie Mercury[2].

Doing All Right
„Doing All Right” został napisany przez Brian Maya i Tim Staffela, jeszcze przed powstaniem Queen. Charakter kompozycji utworu zmienia wielokrotnie, od lekkiego popu przez sekcje z akustyczną gitarą, aż po fragmenty właściwe dla heavy metalu. Jest to jeden z niewielu utworów zespołu, w których Brian May gra na fortepianie. Gra też na swojej dawnej akustycznej gitarze (później w takich utworach jak „White Queen (as it Began)”, „Jealousy”). Queen grał ten utwór w 1970. Jest to pierwszy koncertowy utwór, w którym Freddie zagrał na fortepianie.

Great King Rat
„Great King Rat” został napisany przez Freddiego Mercury’ego. Utwór ten jest przykładem wczesnego brzmienia Queen (długość trwania, mocna kompozycja, gitarowe solo i nagłe zmiany tempa).

My Fairy King
„My Fairy King” został napisany przez Freddiego Mercury’ego. Opowiada o krainie Rhye – fantastycznym świecie stworzonym przez Mercury’ego. „My Fairy King” jest pierwszym utworem, w którym Mercury mógł zaprezentować swoje umiejętności w grze na fortepianie. W utworze „Doing All Right” sekcje na gitarze grał Brian May inspirując się grą Mercury’ego. Od tego momentu Mercury grał większość sekcji fortepianowych.

Roger Taylor śpiewa natomiast w wyższych tonacjach. Overdubbing rzekomo został użyty w wielu następnych utworach zespołu, szczególnie „Bohemian Rhapsody”. Mercury wziął kilka linii tekstu z poematu Roberta Browninga pod tytułem The Pied Piper of Kamelin.

Liar
„Liar” został napisany przez Mercury’ego w 1970 jeszcze pod nazwiskiem Farrokh Bulsara i przed dołączeniem Johna Deacona do zespołu. Jak potwierdzono w kopii zapisów dotyczących nagrania wydanego przez EMI Music, jest to jedno z kilku nagrań Queen z 1970, w których wykorzystano organy Hammonda.

Fani Queen twierdzą, że John Deacon śpiewa linię „all day long”, ponieważ śpiewał on ten fragment na koncertach. Naprawdę jednak nie wiadomo czy Deacon faktycznie śpiewał wokal pomocniczy. W obu wersjach, Deacon śpiewał do mikrofonu Mercury’ego.

The Night Comes Down
Utworów napisał Brian May krótko po utworzeniu zespołu w 1970. Było to pierwsze nagranie w studiu De Lane Lea Studios we wrześniu 1971, gdy zespół został wynajęty do testowania nowego sprzętu w zamian za możliwość wykonania nagrań demonstracyjnych w celu znalezienia firmy nagraniowej. Porozumienie przyniosło dochody i Queen czerpał korzyści z najnowszego sprzętu, by umieścić pięć utworów na kasecie.

W 1972 Trident Studios podpisało z zespołem kontrakt zezwalający na nagrywanie, ograniczający ich dostęp tylko do czasu, w którym nikt z niego nie korzystał (gdy płacący artyści nic nie nagrywali) i wtedy też Queen rozpoczął współpracę z producentem Royem Thomasem Bakerem . Baker i właściciele/zarządzający Norman i Barry Sheffield nalegali, aby ponownie nagrać pięć dem ze studia De Lane Lea.

Nagrana została nowa studyjna wersja „The Night Comes Down”, ale w końcu uznano, że nagranie ze studia De Lane Lea jest najlepsze i jest to właśnie wersja, która znalazła się na debiutanckim albumie. Nieużyta wersja Roya Thomasa Bakera nie została wydana i nie istnieje żaden jej bootleg.

Modern Times Rock ’n’ Roll
Utwór ten śpiewa perkusista Roger Taylor, który też napisał tę piosenkę. Piosenka została nagrana dodatkowo dwa razy dla BBC. Pierwszy raz (dla BBC) w grudniu 1973, i transmitowana w John Peel’s Show, ta wersja została wydana w 1989 na albumie Queen at the Beeb. Drugie nagranie zostało wykonane w 1974, i transmitowane w Bob Harris’s Show. Ta wersja nie ujrzała światła dziennego poza bootlegiem, podczas którego można usłyszeć różnice z pierwotną wersją – bootleg ten ma wolniejsze tempo i dodatkowy wokal Freddiego Mercury’ego.

Son and Daughter
„Son and Daughter” został napisany przez gitarzystę Briana Maya i był umieszczony na odwrocie singla „Keep Yourself Alive”. Został napisany w 1972 i zawiera gitarowe solo Maya. Wersja z albumu jest pozbawiona tego fragmentu. Solo to nie zostało ukończone aż do 1974, gdy użyto go w „Brighton Rock”. Do tego czasu Brian May wykonywał solo w trakcie „Son and Daughter” podczas koncertów, dając reszcie zespołu czas na przebranie się i zmianę kostiumów. Fragment ten można usłyszeć również w dłuższej wersji „Son and Daughter”, którą umieszczono na albumie Queen at the Beeb.

Jesus
Tekst utworu mówi o Jezusie z Nazaretu. Występuje tu sekcja dwuakordowego rytmu podczas wersów, w długim instrumentalnym zakończeniu.

Seven Seas of Rhye
Utwór ten został jedynie częściowo ukończony i umieszczony na pierwszym albumie (jako utwór instrumentalny). Jego pełna wersja znalazła się na kolejnym albumie studyjnym, Queen II.
'''


def ShowInfo(ask):
    check_ALBUM = list(map(lambda x: x.lower(), ALBUM))
    if ask in check_ALBUM:
        print('Informacje o utworze:\n')
        for i in range(check_ALBUM.index(ask) + 1, len(ALBUM)):
            if len(ALBUM[i]) < 50:
                break
            else:
                print(ALBUM[i])
    elif ask == 'lista':
        print('Lista utworów:')
        for a in ALBUM:
            if len(a) < 50:
                print(a)
    else:
        print('Brak takiego utworu\n*wpisz "lista" jeśli chcesz zobaczyć dostępne utwory')


ALBUM = ALBUM.split("\n")
for a in ALBUM:
    if a == '':
        ALBUM.remove(a)
while True:
    ask = input('Podaj nazwę utworu dla: {}\n---napisz "end" aby zakończyć---'.format(DISC)).lower()
    if ask == 'end':
        break
    ShowInfo(ask)


