# TODO


- [ ] G - Administrationssystem för en bank.
    - [x] Inloggning ska vara implementerat
        Du ska lägga in roller via seed, Rollen Cashier ska kunna administrera kunder och deras konton.
    - [x] Använd den databas som seedas vid uppstart, SQLAlchemy etc.
    - [x] Bygg ett webbgränssnitt.
    - [x] Startsida: skriv ut statistik på startsidan. Man ska se antal kunder, antal konton och summan av saldot på konton.
    - [x] Det får inte bli några avrundningsfel så använd decimal.
    - [x] Bygg en Flask lösning för en bank som kan hantera kunder, deras konton med saldo samt transaktioner.
    - [x] Seeda två användare:
        - [x] stefan.holmberg@systementor.se och Hejsan123# och som Admin
        - [x] stefan.holmberg@nackademin.se och Hejsan123# och som Cashier
    - [x] Det ska gå att ta fram en kundbild genom att ange kundnummer.
        - [x] Kundbilden ska visa all information om kunden och alla kundens konton.
        - [x] Kundbilden ska också visa det totala saldot för kunden genom att summera saldot på kundens konton.
        - [ ] När man klickar på ett kontonummer i kundbilden ska man komma till en kontosida som visar kontonummer och saldo samt en lista med transaktioner i descending order.
    - [x] Det ska gå att söka efter kund på namn och stad
        - [x] En lista ska visas med kundnummer och personnummer, namn, adress, city som sökresultat.
        - [x] Sökresultatet ska vara möjligt att sortera. Första klicket på en kolumn = asc, sen desc, sen asc etc etc
        - [x] Sökresultatet ska vara paginerat (50 resultat i taget och så ska man kunna bläddra till nästa/tidigare sida).
        - [x] Klickar man på en kund ska man komma till kundbilden.
    - [ ] Lägg till en kontobild där man kan se transaktioner för ett individuellt konto.
        - [ ] Systemet ska också hantera insättningar, uttag och överföringar mellan konton.
        - [ ] Det ska inte gå att ändra saldo direkt på ett konto - alltid via en transaktion.
        - [ ] Det ska framgå tydligt om någon försöker ta ut eller överföra mer pengar än vad som finns på kontot.
    - [ ] Input valideringar, tänk på att kronofogden ska använda systemet.
    - [ ] Det ska finnas Unit Tester där du skriver tester som testar att det:
        - [ ] inte går att ta ut eller överföra mer pengar än det finns på kontot.
        - [ ] gå att sätta in eller ta ut negativa belopp.
    - [ ] Make it look najs
    - [ ] Dubbelkolla om dom här instruktionerna ens stämmer





- [ ] VG - Lösningen måste vara gjord med god arkitektur.
    - [ ] Det ska gå att skapa en ny och ändra en kund.
        - [ ] När en kund skapas ska de få ett nytt unikt kundnummer.
        - [ ] Det ska automatiskt skapas ett transaktionskonto med kunden som ägare. OBS: inputvalidering (även i browser)
    - [ ] Rollerna Admin och Cashier ska automatiskt skapas i databasen vid uppstart om de inte finns. (Seed)
    - [ ] Om det finns fler än 20 transaktioner ska JavaScript/AJAX användas för att ladda in ytterligare 20 transaktioner när man trycker på
    en knapp längst ned i listan. Trycker man igen laddas 20 till, och så vidare.
    - [ ] Lägg till ett gränssnitt för att CRUDa användare och sätta roller 
    - [ ] Sökresultatet ska vara möjligt att sortera. Första klicket på en kolumn = asc, sen desc, sen asc etc etc.
    - [ ] Startsidan ska gruppera antal kunder, antal konton och summan av saldot på konton per LAND. När man klickar på tex "Norway" ska man komma till en sida där de 10 största (högst totalsaldo) kunderna i det landet visas. 
    - [ ] Banken har också en mobilapp för kunder. Skapa ett Web API till appen.
        - [ ] Ett anrop till /api/<kundid> ska ge samma information som i kundbilden.
        - [ ] Ett antop till /api/accounts/12345 ska visa transaktioner för ett konto. Använd parametrar limit och offset för att begränsa antal transaktioner som hämtas. OBS: Denna kan du använda för AJAX!
    - [ ] Banken har också en Console app (batch som körs varje natt). Det kollar efter misstänkta transaktioner (penningtvätt tex)
    - [ ] Implementera denna så den återanvänder kod. Programmet ska:
        för varje land
            för varje användare i det landet
                för varje kontotransaktion för användaren kolla om den uppfyller regel för "misstänkt" (se nedan)
                "En enskild transaktion större än 15000 kr, eller totala transaktioner de senaste tre dygnen (72h) från aktuellt tidpunkt större än 23000"
        när "landet" är klart skicka en rapport (mail) till <land>@testbanken.se.
        Bara en lista över vilka personer och vilka kontonummer och vilka transaktionenummer
    - [ ] Håll reda på var du slutar sas så du inte börjar från början varje dag
