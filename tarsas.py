import random
import streamlit as st
from PIL import Image, ImageOps

st.set_page_config(
    initial_sidebar_state="expanded",
    layout="centered"
)
def resize_and_pad(image_path, size=(200, 200), bg_color=(255, 255, 255, 0)):
    try:
        img = Image.open(image_path).convert("RGBA")
        img.thumbnail(size, Image.LANCZOS)  # arányosan átméretezi (felnagyít is!)

        background = Image.new("RGBA", size, bg_color)
        offset = ((size[0] - img.width) // 2, (size[1] - img.height) // 2)
        background.paste(img, offset)
        return background
    except Exception as e:
        st.warning(f"Nem sikerült betölteni a képet: {e}")
        return None


# Társasjáték adatbázis
games = [
    {"name": "Társasház", "players": (3, 5), "duration": "30–60 perc", "complexity": "közepes", "style": ["patyjáték", "következtető",  "kártyahúzós", "dedukciós"], "cooperative": False, "image": "games/tarsashaz.png", "rules":"https://www.youtube.com/watch?v=SvuU0Nbl8BY&t=616s", "description": "Egy külvárosi bérház köztudottan gyanús figurák lakóhelye. A rendőrfőnök egy csapat fiatal nyomozót bíz meg a feladattal: találjanak megy egyet-egyet az ismert bűnözők közül. \nEbben a 3-5 játékos számára készült dedukciós partijátékban az egyik játékos a játékmester, aki a bűnözők bőrébe bújva válaszolja meg a nyomozók kérdéseit."},
    {"name": "80 Days", "players": (2, 4), "duration": "30–60 perc", "complexity": "egyszerű", "style": ["családi", "kaland",], "cooperative": False, "rules":"https://www.youtube.com/watch?v=VpslJu-QzyM", "image": "games/80days.png","description": "Izgalmas kalandjaidat követően legyél Te, aki elsőként ér vissza Londonba! 1872. London. Egy őrült fogadás híre robbanásként terjed a városban. A rejtélyes Fogg úr mindössze 80 nap alatt akarja körbe utazni a világot. Elfogadjátok a kihívást és belevágtok az utazásba. Az a célotok, hogy a legtöbb győzelmi pontot szerezzétek. Ehhez a lehető leggyorsabban kell körbe utaznotok a világot, öt perióduson belül vissza kell érkeznetek Londonba, és útközben minél több kalandot kell átélnetek"},
    {"name": "Axio", "players": (1, 4), "duration": "30-60 perc", "complexity": "egyszerű", "style": ["logikai", "absztrakt", "családi"], "cooperative": False, "rules":"https://www.youtube.com/watch?v=JHk3BJ3s6Nk", "image": "games/axio.png", "description": "Az AXIO egy elegáns lapkalerakó játék az egész családnak! A játékban a játékosok célja, hogy az értékjelzőiket az értékelő tábláikon a lehető legmagasabb értékig eljuttassák. Sorban egymás után helyezik le a játéktáblára a lapkákat. Az egyező szimbólumokért pontokat kapnak. A kapott pontokat az értékjelzőikkel jelölik az értékelő tábláikon. A játék végén, az utolsó helyen álló értékjelzők helyét hasonlítják össze. A játékot az nyeri, akinek az utolsó helyen álló értékjelzője a legmagasabb helyen áll."},
    {"name": "Mars terraformálása", "players": (1, 5), "duration": "2+ óra", "complexity": "összetett", "style": ["stratégiai", "versengős", "sci-fi", "építgetős"], "cooperative": False, "rules":"https://www.youtube.com/watch?v=Pn97fYL1RzU", "image": "games/mars.png", "description": "A Mars lakhatóvá tétele : Víz, oxigén, és a megfelelő hőmérséklet...Ez a három dolog, amire biztos, hogy szükség lesz, ha a vörös bolygón képzeljük el a jövőt. Biztosítsd ezekből Te a legtöbbet, és tedd lakhatóvá a Marsot!"},
    {"name": "7 Csoda", "players": (2, 7), "duration": "30–60 perc", "complexity": "közepes", "style": ["draft", "stratégiai", "versengős", "építgetős"], "cooperative": False, "rules":"https://www.youtube.com/watch?v=SzJ4QnKOKxo", "image": "games/7csoda.png", "description": "Építsd fel az ókori világ hét csodájának egyikét! Hozd meg a megfelelő döntéseket és teremts egy virágzó civilizációt ebben a rendkívül pörgős, színes, ötletes civilizációs kártyajátékban. De ne feledd, a csoda megépítése csak az egyik útja a pontszerzésnek. Rengeteg izgalom, taktika és stratégia, egy mindössze félórás játékban!"},
    {"name": "Bűnügyi krónikák", "players": (1, 4), "duration": "60-120 perc", "complexity": "közepes", "style": ["történetvezérelt", "kooperatív", "nyomozós"], "cooperative": True, "rules":"", "image": "games/bunugyi.png", "description": "Oldjatok meg szövevényes bűneseteket, járjátok be a tetthelyeket élőben! A Bűnügyi krónikák a nyomozás kooperatív játéka, egy alkalmazás, egy társasjáték és a virtuális valóság tökéletes kombinációjával."},
    {"name": "Utolsó péntek", "players": (2, 6), "duration": "30–60 perc", "complexity": "közepes", "style": ["történetvezérelt", "versengős", "rejtvényes", "horror"], "cooperative": False,"rules":"", "image": "games/utolso.png", "description": "AZ UTOLSÓ PÉNTEK egy horrorjáték, amely egy elátkozott nyári táborban játszódik. Ez a történet egy halálból visszatért eszelősrő szól... 1980 nyara.Egy erdei tábor új tulajdonosai felfogadtak öt barátot tanácsadónak, hogy az ingyenes nyaralásért cserébe rendbe tegyék a birtokot... de most már csak a hétvégét próbálják túlélni."},
    {"name": "Mysterium", "players": (2, 7), "duration": "30–60 perc", "complexity": "közepes", "style": ["kooperatív", "rejtély", "vizuális"], "cooperative": True,"rules":"", "image": "games/mysterium.png", "description": "Mentalisták, spiritiszták és jósnők, eljött az idő!A Warwick kúria már több éve teljesen elhagyatott, mióta a ház urát meggyilkolták. Bár a nyomozás sokáig zajlott és kimerítő volt, mégsem találták meg a tettest. Azóta a ház lassan, de biztosan romlásnak indult és azt suttogják, Lord Warwick szelleme a mai napig a falak között kísért… A Mysterium egy aszimmetrikus kooperatív társasjáték, melyben a résztvevőknek lehetőségük van a világ minden tájáról érkező jósok bőrébe bújni, hogy a Warwick Kúria titkára fényt derítsenek és megadják a benne kísértő szellemnek a végső nyugodalmat. A 2-7 főig játsztató társasban egy személy a szellemet fogja alakítani, és álmokkal próbálja rávezetni a ház ideiglenes lakóit a titok megoldására"},
    {"name": "Harry Potter: Halálfalók felemelkedése", "players": (2, 4), "duration": "60–120 perc", "complexity": "közepes", "style": ["kooperatív", "kaland", "tematikus"], "cooperative": True, "rules":"", "image": "games/halalfalok.png", "description": "A Sötét varázslatok kivédése órák anyagának elsajátítása után ideje szembeszegülni a Sötét Nagyúrral, és megakadályozni a Halálfalók felemelkedését! Mindig is arról álmodtál, hogy a Roxfort Boszorkány-és Varázslóképző iskolába jársz, ahol menő varázslatokat tanulnál és vicces bájitalokat kotyvasztanál? Vagy ennél bátrabb lennél, és te is szembeszállnál a Sötét Nagyúrral? A Halálfalók felemelkedése társasjátékban ezt most megteheted, ugyanis átélheted azokat a nehézségeket és borzalmakat, amikkel az ötödik évfolyamba járó Harry-nek, Hermione-nak és Ron-nak kellett megküzdenie!"},
    {"name": "Csodaország csatái", "players": (2, 5), "duration": "60–120 perc", "complexity": "összetett", "style": ["kártyajáték", "stratégiai", "fantasy"], "cooperative": False, "rules":"", "image": "games/csodaorszag.png", "description": "Hódítsd meg Csodaországot! A Csodaország csatái összetett, kockázatvállalós stratégiai társasjáték. A játékosok egyedi képességeiket használva csatlósokat toboroznak, és remélik, hogy azokat be is tudják vetni... Csodaország bolondos hely…volt valaha. De azóta minden megváltozott. A tarka világbólcsatatérlett. Alice, a Vörös Királynő, a Kalapos, Vigyori úr és a Gruffacsór egy végzetes teapartin toboroznak sereget egymás ellen, és vezénylik őket a könnytótól a beszélővirágok kertjén át a kuszmadt fákfelé."},
    {"name": "Coffee Rush", "players": (2, 4), "duration": "15–30 perc", "complexity": "egyszerű", "style": ["gyors", "ügyességi", "gyerekbarát"], "cooperative": False, "rules":"", "image": "games/coffeerush.png", "description": "Siess, nehogy lefőzzenek! A Coffee Rush szép kivitelű, pörgős családi társasjáték. A játékosok italmegrendeléseket igyekeznek teljesíteni, mielőtt a megrendelők elunják a várakozást..."},
    {"name": "Műgyűjtők társasága", "players": (2, 4), "duration": "30–60 perc", "complexity": "közepes", "style": ["stratégiai", "családi"], "cooperative": False, "rules":"", "image": "games/mugyujtok.png", "description": "Legyen a tiéd a legmenőbb galéria! A Műgyűjtők társasága művészi lapkalehelyezős, licitálós családi társasjáték. A játékosok a magángalériájukat rendezik be csodálatos festményekkel – szigorú ízlésbéli szabályok alapján. El tudsz képzelni egy nappalit, ahol Klimt, Picasso, Hokusai, és van Gogh képek lógnak a falon? Hogy rendeznéd be? Nyilván fontos az ízléses elrendezés, ha le akarod nyűgözni műkedvelő barátaidat!"},
    {"name": "Gyűrűk Ura: Párbaj", "players": (2, 2), "duration": "15–30 perc", "complexity": "egyszerű", "style": ["duell", "fantasy", "kártyajáték"], "cooperative": False, "rules":"", "image": "games/7csodaparbaj.png", "description": "Középfölde sorsa a Ti kezetekben van! A Gyűrűk Ura – Párbaj Középföldéért kétfős stratégiai társasjáték tapasztaltabb játékosok számára is. A játékosok a Szövetséget, illetve Szauron erőit irányítva igyekeznek felszabadítani vagy leigázni Középfölde népeit. A díjnyertes 7 Csoda – Párbaj tematikus változata."},
    {"name": "Tea Time Crime", "players": (2, 4), "duration": "15–30 perc", "complexity": "egyszerű", "style": ["deduktív", "gyors", "könnyed"], "cooperative": False, "rules":"", "image": "games/teatimecrime.png", "description": "Előkelő látogatók a tiszteletreméltó Longshore vidéki birtokon - meg kell védeni a nemes vendégek értékeit.Ehhez ügyesen kell elhelyezni a detektíveket és el kell kapni a tolvajokat! Lord Waldemar és elit vendégei hálásak lesznek majd, ha gondoskodtok a ház biztonságáról."},
    {"name": "Sequence", "players": (2, 12), "duration": "15–30 perc", "complexity": "egyszerű", "style": ["kártyás", "logikai", "családi"], "cooperative": False, "rules":"", "image": "games/sequence.png", "description": "Izgalmas stratégiai játék, amelyben kártyát játszunk ki, majd lehelyezünk a táblára egyik zsetonunkat és mikor kigyűlt 5 egy sorban, akkor már nyertél is! Ne habozz a társaid blokkolásában, sőt vedd le a zsetonjukat is. Egy csipetnyi stratégia szerencsével fűszerezve a siker receptje!"},
    {"name": "Mr. Jack", "players": (2, 2), "duration": "15–30 perc", "complexity": "közepes", "style": ["logikai", "duell", "nyomozós"], "cooperative": False, "rules":"", "image": "games/mrjack.png", "description": "1898 - Whitechapel, London Az éjszaka leple borítja sötétségbe a sikátorokat, csak néhány helyen pislákolnak a lámpások. Nyolc nyomozó gyűlt össze, hogy elkapják közösen Mr Jack-et, aki még mindig szabadlábon van. De Mr Jack okosabb, mint gondolnák - hiszen ő az egyik közülük! Ha Jack-et játszod, akkor menekülj el a nyomozótól még napfelkelte előtt, vagy hagyd el a várost a sötétséget kihasználva! Ha pedig a detektív vagy, akkor próbáld meg leleplezni Mr Jack-et még mielőtt felkel a Nap!"},
    {"name": "Ticket to Ride: Paris", "players": (2, 4), "duration": "15–30 perc", "complexity": "egyszerű", "style": ["családi", "útvonalépítős"], "cooperative": False, "rules":"", "image": "games/tickettoride.png", "description": "Fedezzétek fel Párizs látványosságait! A Ticket to Ride: Párizs egyszerű szabályú, gyorsan lejátszható, változatos családi társasjáték. A játékosok különböző színű jegyek begyűjtésével és kijátszásával igyekeznek a többieknél gyorsabban bejárni Párizs látványosságait."},
    {"name": "Shadows: Amszterdam", "players": (4, 8), "duration": "15–30 perc", "complexity": "egyszerű", "style": ["kooperatív", "asszociációs", "családi"], "cooperative": True, "rules":"", "image": "games/amszterdam.png", "description": "Vajon hova vezet minket a csapatvezetőnk az új képpel? A korláttal a hídra utal, vagy a kerek ablakkal a holdas lapra? Két csapat verseng egymással, melyikőjük talál meg hamarabb három pontot a képek alkotta Amsterdam-ban. A csapatjelző bábu csak egyet vagy kettőt léphet, attól függően, egy vagy két kártyát kaptak-e utalásként. A játék nincs körökre bontva, így az a csapat nyer, amelynek a vezetője hamarabb talál összefüggést a célterület és a 10 felcsapott kép között, illetve hogy a csapat milyen hamar jön rá, hova kell lépniük. Egy színes és vidám asszociációs partijáték - győzzön a gyorsabb csapat!"},
    {"name": "Kartográfusok", "players": (1, 100), "duration": "30–60 perc", "complexity": "közepes", "style": ["rajzolós", "flip-and-write", "stratégiai"], "cooperative": False, "rules":"", "image": "games/kartografusok.png", "description": "Ahogy Nalos határai egyre messzebbre nyúlnak, úgy egyre nagyobb a veszély is, mely a királyságot fenyegeti. Sorra érkeznek a bátor hősök, de vajon lesz-e elég erejük megküzdeni a rajtuk ütő szörnyetegekkel..? Bár az északi földterületeken nagy megtiszteltetésnek számít térképészeti munkát végezni, sajnos az expedíciókon való részvétel egyre veszélyesebbé vált az utóbbi időkben. Szerencsére a Gimnax királynőhöz hűséges hősök bátran szembeszállnak a fenyegető Dragul hordákkal! Használd ki a bátor lovagok erősségeit, és terjeszd ki Nalos Királyságának területét – a királynő dicsőségére!"},
    {"name": "Bang! Kockajáték", "players": (3, 8), "duration": "15–30 perc", "complexity": "egyszerű", "style": ["party", "rejtett szerepes", "western"], "cooperative": False,"rules":"", "image": r"games/bang.png", "description": "Pörgős vadnyugati kockajáték, amiben nem tudhatod biztosan, kik az ellenségeid...  A Bang! Kockajáték népszerű, titkos szerepes partijáték. Ebben a társasjátékban a játékosok a vadnyugat hőseinek és banditáinak bőrébe bújnak, és a kockák gurításával igyekeznek leszámolni ellenségeikkel. "},
    {"name": "Sherlock (kártyás)", "players": (2, 4), "duration": "15–30 perc", "complexity": "közepes", "style": ["kooperatív", "nyomozós", "történetvezérelt"], "cooperative": True, "rules":"", "image": "games/sherlock.png", "description": "Sherlock Holmes, John Watson, James Moriarty, Irene Adler… Az ismert hősökre a gyanú árnyéka vetül - egyikük bűnöző. Melyikőtök oldja meg a rejtvényt, és nevezi meg a törvénytisztelő állampolgárok közt megbújó gonosztevőt? A Sherlock a Kalandra fel! társasjátékcsalád első darabja. A játékosok egymással versengenek, hogy felderítsék a rejtélyt és megnevezzék a gonosztevőt: logikus gondolkodással, pontos ténymegállapítással és helyes következtetésekkel lehet csak övék a győzelem. Remek agytorna minden ifjú detektívnek."},
    {"name": "Időzített bomba", "players": (4, 8), "duration": "15–30 perc", "complexity": "egyszerű", "style": ["party", "rejtett szerepes"], "cooperative": False, "rules":"", "image": "games/bomba.png", "description": "Még tíz másodperc! Melyiket vágjam el?! Méltóságteljesen magasodik a Temze fölé a stabilitás szimbóluma, a Big Ben. Harangjátékát minden este mosolyogva hallgatják a helybéliek. De ma a torony táncoló inga-monstrumai közt valami nagyon nincs rendben. Moriarty társaival egy időzített bombát rejtett el a fogaskerekek labirintusában, és már csak a nagy Sherlock és csapata lehet az, aki időben megtalálhatja, és hatástalaníthatja a pokolgépet."},
    {"name": "Fogd a szappant!", "players": (3, 6), "duration": "15–30 perc", "complexity": "egyszerű", "style": ["party", "gyors", "humoros"], "cooperative": False, "rules":"", "image": "games/fogdaszappant.png", "description": "Partyjáték a felnőtt korosztálynak! Ebben a dilis humorú kártyajátékban nincsenek nyertesek, csak egyetlen vesztes, akinek fel kell vennie a szappant. Jellegzetes illusztrációival, rendhagyó humorával kitűnik nem csak a játékasztalon, de a polcokról is, és biztosan a felnőttjátékok királya lesz a bulikon!"},
    {"name": "UNO Teams", "players": (2, 10), "duration": "15–30 perc", "complexity": "egyszerű", "style": ["kártyajáték", "családi", "gyerekbarát"], "cooperative": False, "rules":"", "image": "games/unoteams.png", "description": "Az UNO Teams egy új módja a klasszikus játék élvezetének! A játékosok továbbra is színek, számok és szimbólumok szerint rakják le a lapokat, de ezúttal nem mindenki önállóan játszik, hanem párokban, csapatként küzdenek a győzelemért. Különleges kártyák és szabályok segítik a csapattársakat az együttműködésben, de a győzelemhez mindkét játékosnak meg kell szabadulnia az összes lapjától."},
    {"name": "Spot It", "players": (2, 8), "duration": "15–30 perc", "complexity": "egyszerű", "style": ["ügyességi", "gyerekbarát", "gyors"], "cooperative": False, "rules":"", "image": "games/spotit.png", "description": "A Spot it pörgős, zsebre vágható kártyajáték 5-féle játékváltozattal. A kártyákon 8-8 különböző képecske látható, és bármelyik két kártyán mindig van egy ugyanolyan belőlük. A játékosok feladata, hogy a többieknél gyorsabban megtalálják a közös képeket. A koncentrációt és a reflexeket fejlesztő társasjáték."},
    {"name": "Magyar kártya", "players": (2, 16), "duration": "15–30 perc", "complexity": "egyszerű", "style": ["klasszikus", "versengős"], "cooperative": False, "rules":"", "image": "games/magyar.png", "description": ""},
    {"name": "Ligretto (3 doboz)", "players": (2, 12), "duration": "15–30 perc", "complexity": "egyszerű", "style": ["gyors", "reakcióidő", "party"], "cooperative": False, "rules":"", "image": "games/ligretto.png", "description": "A Ligretto egy gyors kártyajáték, amely bármely korosztály számára remek szórakozás. Leülhet egy asztalhoz akár az egész család, senki sem fog unatkozni. A játékban a legfontosabb a gyorsaság. A lapokon lévő színek és számok egyaránt számítanak. A partit az kezdi, aki birtokolja az 1-es kártyalapot. Ezt követően minden játékos egyidejűleg próbálja meg lerakni a sorban következő és színben egyező lapjait. A gyorsaság dönt, ki teheti le végül a kártyát, a keresést azonban megnehezíti, hogy a kártyákat több helyen kell tartani, és sok esetben nem is lehet megnézni minden lapot. A végén pontozással dől el, ki a nyertes. A szabályok könnyen elsajátíthatók. A játék gyors, koncentrációt igényel, de közben szórakoztató és rendkívül izgalmas."},
    {"name": "Francia kártya", "players": (2, 16), "duration": "15–60 perc", "complexity": "egyszerű", "style": ["klasszikus", "kártyajáték"], "cooperative": False,"rules":"", "image": "games/francia.png", "description": ""},
    {"name": "Sole mio", "players": (2,2), "duration": "15–30 perc", "complexity": "egyszerű", "style": ["kártyajáték", "családi", "memóriajáték"], "cooperative": False,  "rules":"","image": "games/solemio.png", "description": "Szereted a pizzát? És sütöttél már valaha egyet is, vagy inkább rendelsz egyet a kedvenc pizzériádból? Most itt az alkalom, hogy te is kipróbáld magad pizzakészítőként! Játszd ki megfelelő sorrendben a hozzávalók kártyáit a kezedből a többiekkel közös pakliba, és ha mindenből eleget gyűjtöttetek, csapj le rá a teljesítendő rendeléskártyáid valamelyikével! Vajon jól emlékeztél, és sikerült a megfelelő alapanyagokat összegyűjteni? Egy pizzasütésnyi idő múlva kiderül!"},
    {"name": "Szócsapdák", "players": (4,12), "duration": "15–30 perc", "complexity": "egyszerű", "style": ["party", "családi", "kooperatív"], "cooperative": True, "rules":"", "image": "games/szocsapdak.png", "description": "Két csapat, egy cél: vajon ki teljesíti hamarabb? Ki a jobb szóalkotó? Már csak egy kamra választ el minket a szörnytől... Itt a varázsszó, ami nyitja, de vajon milyen csapdákkal védte le a másik csapat?!"},
    {"name": "Corsari", "players": (2,4), "duration": "15–30 perc", "complexity": "egyszerű", "style": ["kártyajáték", "családi", "taktikai"], "cooperative": False, "rules":"", "image": "games/corsaris.png", "description": ""},
    {"name": "Roxforti csata", "players": (2,5), "duration": "60–120 perc", "complexity": "közepes", "style": ["deck building", "kooperatív", "tematikus"], "cooperative": True, "rules":"", "image": "games/roxfort_nagy.png", "description": "A játékosok a Roxforti csata társasjátékkal a Roxfort Varázsló-és Boszorkányképzőben zajló epikus csatát - és az odáig vezető eseményeket - élhetik át. A gonosz erők visszaverése és az iskola biztonsága négy tanuló együttműködésén múlik - a játékosoknak Harry, Ron, Hermione és Neville szerepébe bújva kell minél jobb paklit építeniük, és a megszerzett kártyák segítségével legyőzni az ellenfeleket.Tanulj új varázslatokat, szerezz mágikus tárgyakat, és közben akadályozd meg, hogy a Halálfalók megerősödjenek!"},
    {"name": "Roxforti csata - Sötét varázslatok kivédése", "players": (2,2), "duration": "30–60 perc", "complexity": "közepes", "style": ["deck building", "taktikai", "tematikus"], "cooperative": False, "rules":"", "image": "games/roxfort_kicsi.png", "description": "A varázslóvilág félelemben és rettegésben él, napjaik kilátástalanok...De felcsillan a remény! Vajon tudsz segíteni a varázslók és boszorkányok megmentésében? A Reggeli Prófétában mindennaposak a borzalmas hírek, ezért Dumbledore professzor úgy döntött, párbajszakkört indít. Hiszen mindenkire szükség van ahhoz, hogy ezt az ádáz harcot megnyerjük! Tartsatok velünk, hogy felkészülhessetek a Sötét varázslatok kivédésére!"},
    {"name": "Azul párbaj", "players": (2, 2), "duration": "15–30 perc", "complexity": "egyszerű",
     "style": ["absztrakt", "taktikai", "kooperatív"], "cooperative": False, "rules": "", "image": "games/azul_parbaj.png",
     "description": "Két csapat, egy cél: vajon ki teljesíti hamarabb? Ki a jobb szóalkotó? Már csak egy kamra választ el minket a szörnytől... Itt a varázsszó, ami nyitja, de vajon milyen csapdákkal védte le a másik csapat?!"},
    {"name": "Zamatkockák", "players": (2, 4), "duration": "15–30 perc", "complexity": "egyszerű",
     "style": ["kockajáték", "családi", "taktikai"], "cooperative": False, "rules": "", "image": "games/zamatkockak.png",
     "description": ""},
    {"name": "Coffee rush Hab a tortán", "players": (2, 4), "duration": "60–120 perc", "complexity": "egyszerű",
     "style": ["deck building", "kooperatív", "tematikus"], "cooperative": True, "rules": "",
     "image": "games/hab_a_tortan.png",
     "description": "A játékosok a Roxforti csata társasjátékkal a Roxfort Varázsló-és Boszorkányképzőben zajló epikus csatát - és az odáig vezető eseményeket - élhetik át. A gonosz erők visszaverése és az iskola biztonsága négy tanuló együttműködésén múlik - a játékosoknak Harry, Ron, Hermione és Neville szerepébe bújva kell minél jobb paklit építeniük, és a megszerzett kártyák segítségével legyőzni az ellenfeleket.Tanulj új varázslatokat, szerezz mágikus tárgyakat, és közben akadályozd meg, hogy a Halálfalók megerősödjenek!"},
    {"name": "Moving day", "players": (2, 4), "duration": "15–30 perc", "complexity": "egyszerű",
     "style": ["kockajáték", "családi", "taktikai"], "cooperative": False, "rules": "", "image": "games/moving.png",
     "description": ""},
]

# Oldalsáv kérdések
st.sidebar.title("🎲 Kérdőív")
all_games=st.sidebar.checkbox("Összes játék mutatása")
num_players = st.sidebar.slider("Hányan játszanátok?", 1, 10, 4)
play_time = st.sidebar.selectbox("Mennyi időtök van?", ["15–30 perc", "30–60 perc", "60–120 perc", "2+ óra"])
style_pref = st.sidebar.multiselect("Milyen típusú játékra vágytok?", ["party", "stratégiai", "kooperatív", "versengős", "gyerekbarát", "történetvezérelt", "logikai", "kártyajáték", "gyors"])
complexity_pref = st.sidebar.radio("Milyen bonyolultságú legyen a játék?", ["egyszerű", "közepes", "összetett"])
only_one = st.sidebar.checkbox("Csak egy játékot ajálj")

# Főcím
st.title("🎉 Melyik társasjáték legyen ma?")

# Ajánló logika
def matches(game):
    min_p, max_p = game["players"]
    if not (min_p <= num_players <= max_p):
        return False
    if play_time != game["duration"]:
        return False
    if complexity_pref != game["complexity"]:
        return False
    if style_pref:
        if not any(s in game["style"] for s in style_pref):
            return False
    return True

if all_games:
    matched_games = games
else:
    matched_games = [game for game in games if matches(game)]

if matched_games and only_one:
    matched_games = [random.choice(matched_games)]


# Eredmény
if matched_games:
    st.subheader("🧠 Ajánlott játék(ok):")
    for game in matched_games:
        st.markdown(f"### 🎲 {game['name']}", help=game['description'])
        col1, col2 = st.columns([1, 2])

        with col1:
            st.write(f"- 👥 Játékosszám: {game['players'][0]}–{game['players'][1]}")
            st.write(f"- ⏱️ Játékidő: {game['duration']}")
            st.write(f"- 🧠 Komplexitás: {game['complexity'].capitalize()}")
            st.write(f"- 🎯 Stílus: {', '.join(game['style'])}")
            st.markdown(
                f'''
                - <a href="{game["rules"]}" target="_blank" style="text-decoration: none; color: inherit;">
                    📖 Szabályzat
                </a>
                ''',
                unsafe_allow_html=True
            )
        with col2:
            img = resize_and_pad(game["image"], size=(180, 180))
            if img:
                st.image(img)

else:
    st.warning("Sajnos nincs olyan játék, ami minden feltételnek megfelelne. Próbálj meg kevesebb szűrőt használni!")

