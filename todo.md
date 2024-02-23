# TODO

- [ ] Bild bäckground vore najs
- [ ] Decimal accuracy
- [ ] Fråga när den ska vara klar, hur exakt den ska lämnas in

- [ ] G - Administrationssystem för en bank.
    - [x] Inloggning ska vara implementerat
        Du ska lägga in roller via seed, Rollen Cashier ska kunna administrera kunder och deras konton.
    - [ ] Använd den databas som seedas vid UPPSTART, SQLAlchemy etc.
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
        - [x] När man klickar på ett kontonummer i kundbilden ska man komma till en kontosida som visar kontonummer och saldo samt en lista med transaktioner i descending order.
    - [x] Det ska gå att söka efter kund på namn och stad
        - [x] En lista ska visas med kundnummer och personnummer, namn, adress, city som sökresultat.
        - [x] Sökresultatet ska vara möjligt att sortera. Första klicket på en kolumn = asc, sen desc, sen asc etc etc
        - [x] Sökresultatet ska vara paginerat (50 resultat i taget och så ska man kunna bläddra till nästa/tidigare sida).
        - [x] Klickar man på en kund ska man komma till kundbilden.
    - [x] Make it look najs
    - [x] Lägg till en kontobild där man kan se transaktioner för ett individuellt konto.
        - [ ] Systemet ska också hantera insättningar, uttag och överföringar mellan konton.
        - [x] Det ska inte gå att ändra saldo direkt på ett konto - alltid via en transaktion.
        - [x] Det ska framgå tydligt om någon försöker ta ut eller överföra mer pengar än vad som finns på kontot.
    - [ ] Input valideringar, tänk på att kronofogden ska använda systemet.
    - [ ] Det ska finnas Unit Tester där du skriver tester som testar att det:
        - [ ] inte går att ta ut eller överföra mer pengar än det finns på kontot.
        - [ ] gå att sätta in eller ta ut negativa belopp.
    - [ ] Dubbelkolla om dom här instruktionerna ens stämmer