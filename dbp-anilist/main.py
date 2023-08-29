from flask import Flask, request, jsonify, render_template

anime_database = [
    {"id": 0, "title": "ONE PIECE", "genres": ["action","adventure","comedy","drama","fantasy"], "rating": 87, "reviews": ["The Greatest Adventure Story of All Time"], "episodes": 1074, "format": "tv show", "poster": "https://s4.anilist.co/file/anilistcdn/media/anime/cover/large/nx21-tXMN3Y20PIL9.jpg"},
    {"id": 1, "title": "Gintama: THE FINAL", "genres": ["action","comedy","drama","sci-fi"], "rating": 91, "reviews": ["Gintama: The jewel in the crown of the comedy genre"], "episodes": 1, "format": "movie", "poster": "https://s4.anilist.co/file/anilistcdn/media/anime/cover/large/bx114129-RLgSuh6YbeYx.jpg"},
    {"id": 2, "title": "Fruits Basket: The Final", "genres": ["comedy","drama","psychological","romance","slice of life"], "rating": 90, "reviews": ["Fruits basket the final is a beautiful conclusion"], "episodes": 13, "format": "tv show", "poster": "https://s4.anilist.co/file/anilistcdn/media/anime/cover/large/bx124194-pWfBqp3GgjOx.jpg"}
]

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/anime")
def get_animes():
    return jsonify(anime_database)


@app.route("/anime/<int:id>")
def get_anime(id):
    anime = next((_anime for _anime in anime_database if _anime["id"] == id), None)
    return jsonify(anime) if anime else jsonify({"error": "Anime not found"})


@app.route("/anime", methods=["POST"])
def post_anime():
    new_anime = {
        "id": request.json.get("id"),
        "title": request.json.get("title"),
        "genres": request.json.get("genres"),
        "rating": request.json.get("rating"),
        "reviews": request.json.get("reviews"),
        "episodes": request.json.get("episodes"),
        "format": request.json.get("format"),
        "poster": request.json.get("poster")
    }

    if not all(new_anime.values()):
        return jsonify({"error": "Incomplete anime data"}), 400

    if any(_anime["id"] == new_anime["id"] for _anime in anime_database):
        return jsonify({"error": "Anime with the same ID already exists"}), 409

    anime_database.append(new_anime)
    return jsonify(new_anime), 201


@app.route("/anime/<int:id>", methods=["PUT"])
def put_anime(id):
    global anime_database
    
    anime_to_update = next((_anime for _anime in anime_database if _anime["id"] == id), None)
    
    if anime_to_update:
        updated_data = request.json
        anime_to_update.update(updated_data)
        
        return jsonify({"message": "Anime updated successfully"})
    else:
        return jsonify({"error": "Anime not found"}), 404

        

@app.route("/anime/<int:id>", methods=["PATCH"])
def patch_anime(id):
    global anime_database
    
    anime_to_patch = next((_anime for _anime in anime_database if _anime["id"] == id), None)
    
    if anime_to_patch:
        updated_data = request.json
        
        for key, value in updated_data.items():
            if key in anime_to_patch:
                anime_to_patch[key] = value
        
        return jsonify({"message": "Anime patched successfully"})
    else:
        return jsonify({"error": "Anime not found"}), 404


@app.route("/anime/<int:id>", methods=["DELETE"])
def delete_anime(id):
    global anime_database
    
    anime_to_delete = next((_anime for _anime in anime_database if _anime["id"] == id), None)
    
    if anime_to_delete:
        anime_database.remove(anime_to_delete)
        return jsonify({"message": "Anime deleted successfully"})
    else:
        return jsonify({"error": "Anime not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)













