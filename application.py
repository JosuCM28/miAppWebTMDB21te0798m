from flask import Flask, render_template, make_response
import urllib.request, json, os
from urllib.error import HTTPError, URLError

app = Flask(__name__)

@app.route("/")
def get_movies():
    api_key = os.environ.get("TMDB_API_KEY")
    if not api_key:
        # Mensaje claro si no has configurado la variable en Azure
        return make_response("TMDB_API_KEY no configurada en App Settings.", 500)

    url = f"https://api.themoviedb.org/3/discover/movie?api_key={api_key}"

    try:
        with urllib.request.urlopen(url, timeout=15) as response:
            data = response.read()
    except HTTPError as e:
        # Log simple al navegador; en productivo, usar logging
        return make_response(f"Error HTTP al consultar TMDB: {e.code}", 502)
    except URLError as e:
        return make_response(f"No se pudo contactar TMDB: {e.reason}", 502)
    except Exception as e:
        return make_response(f"Error inesperado al llamar TMDB: {e}", 500)

    try:
        payload = json.loads(data)
    except Exception as e:
        return make_response(f"Respuesta de TMDB no es JSON válido: {e}", 502)

    movies = payload.get("results", [])
    # Evita KeyError si TMDB regresó un error con otro formato
    return render_template("movies.html", movies=movies)

if __name__ == "__main__":
    app.run(debug=False)  # en Azure usa gunicorn
