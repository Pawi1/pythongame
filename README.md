# Projekt dla prof. Pastwa - Gra Web z wykorzystaniem interpretatora Python
## TODO:
- [x] Back-end: web interpretator Pythona
- [x] Zabezpieczenie przed niebezpiecznym kodem od usera
- [x] Hosting itp.
- [x] Skonfigurowanie Django tak że działa i można pracować (dodatkowe pliki,html itp.)
- [ ] Dodanie obsługi Codemirror 
- [ ] Napisanie szablonu ( ludzik, gotowy codemirror, bootstrap(?) )
- [ ] Wymyślenie zadań
- [x] Wymyślnenie fabuły, myśle że nw coś związanego z kosmosem, nw latasz statkiem kosmicznym i tam robisz różne zadania
- [ ] Back-end: sprawdzanie poprawności zadań danych przez usera
- [ ] Zapisywanie postępu w plikach cookies


### FAQ:
___
### 1. Jak uruchomić serwer lokalnie? 
> Zakładam że python jest pobrany
>  1. `pip install -r requirements.txt`
>  2. `python manage.py collectstatic`
>  3. `python manage.py runserver --insecure` 
> dla DEBUG = false
>  4. `python manage.py runserver` 
> dla DEBUG = true
### 2. Git
> Jakieś podstawowe komendy aby można było pracować
>  1. `git clone https://github.com/Pawi1/pythongame/tree/main`
>  2. `git add .`
>  3. `git commit -m "Wiadomość commitu np. Dodanie obsługi Codemirror"`
>  4. `git push`
>  5. `git reset --hard HEAD` cofnięcie zmian lokalnie
>  6. `git status`
>  7. `git config --global user.email "user@example.com"`
>  8. `git config --global user.name "user"`
### 3. Gdzie dodać pliki HTML, CSS, IMG itp?
> HTML >> ./gra/templates/przykladowa_podstrona.html
> * Aby html działał poprawinie trzeba pierw skonfigurować poprawnie django
>
> CSS >> ./gra/static/css/przykladowe_style.css
>
> IMG >> ./gra/static/img/obrazek.png
> #### Aby zadeklarować pliki css,img,js itp. najpierw trzeba poprawnie skonfigurować html:
> ``{% load static %}`` w ``<head>``
## Jak masz jakieś pytania jak coś napisać w Django, pisz do mnie albo skorzystaj z internetu/chatgpt.
