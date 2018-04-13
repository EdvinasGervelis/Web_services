Darbą atliko Edvinas Gervelis. Web servisas - elektronikos parduotuvė.

Servisas pasiekiamas localhost:5000/items.

Galima atlikti GET POST PUT PATCH DELETE.

Papildyta vartotojų servisu. 

Kiekvina prekė turi uzsakymus, kuriuose saugomi uzsakovų ID

Uzsakovo duomenys gali būti pasiekiami:

localhost:5000/items/<item_id>/orders/<customer_id>

Visi prekės užsakovai gali būti pasiekiami

localhost:5000/items/<item_id>/orders

Usakovo duomenys gali būti ištrinami atliekant DELETE adresu :

localhost:5000/items/<item_id>/orders/<customer_id>

Paleidomo komandos:

$ docker-compose build

$ docker-compose up
