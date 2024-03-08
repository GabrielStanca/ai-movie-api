# Cerințe Proiect Sistem de Recomandare Filme

## Descriere Generală

Scopul acestui proiect este de a dezvolta un sistem AI de recomandare a filmelor care poate fi accesat printr-o aplicație web React. Sistemul va putea interpreta cererile utilizatorilor exprimate în limbaj natural pentru a face recomandări de filme relevante, fără a se baza pe întrebări sau răspunsuri statice.

## Funcționalități Principale

- **Interfață React**: Utilizatorii vor interacționa cu AI-ul prin intermediul unei aplicații web dezvoltate în React.
- **Interpretarea Textului**: AI-ul va putea interpreta textul primit de la utilizatori pentru a deduce preferințele acestora.
- **Flexibilitate în Comunicare**: Comunicarea cu AI-ul trebuie să fie flexibilă, fără a se limita la un set fix de întrebări sau răspunsuri.

## Cerințe Tehnice

- **Bază de Date de Filme**: Sistemul va utiliza o bază de date extensivă de filme, cum ar fi setul de date MovieLens sau IMDb, pentru a avea o varietate largă de date.
- **Preprocesare Date**: Datele vor fi curățate și pregătite pentru analiză, inclusiv manipularea genurilor de filme și a ratingurilor.
- **Sistem de Recomandare**: Se va implementa un sistem de recomandare care poate utiliza filtrarea bazată pe conținut, filtrarea colaborativă sau metode hibride.
- **NLP pentru Interpretarea Cererilor**: Se va folosi procesarea limbajului natural (NLP) pentru a interpreta cererile utilizatorilor.
- **API pentru Interfața cu Aplicația React**: Sistemul de recomandare va fi accesibil printr-un API dezvoltat cu FastAPI, cu care aplicația React va comunica.
- **Soluționarea Problemelor CORS**: API-ul va include middleware pentru gestionarea politicii CORS, permițând astfel cererile cross-origin din aplicația React.
- **Antrenabilitate**: AI-ul va putea fi antrenat sau recalibrat pentru a îmbunătăți acuratețea recomandărilor pe baza feedback-ului și a interacțiunilor utilizatorilor.

## Pachete și Dependințe

Pentru dezvoltarea și executarea proiectului sunt necesare următoarele pachete:

- `pandas`: pentru manipularea datelor
- `numpy`: pentru operații numerice
- `scikit-learn`: pentru calculul similarității cosine și alte operațiuni de machine learning
- `fastapi`: pentru crearea API-ului
- `uvicorn`: pentru rularea serverului FastAPI
- `python-multipart`: (opțional) dacă se gestionează date de tip formular

Pentru instalarea tuturor dependințelor, se va crea un fișier `requirements.txt` și se vor instala folosind comanda `pip install -r requirements.txt`.
