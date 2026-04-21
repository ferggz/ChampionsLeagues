from flask import Flask, render_template

app = Flask(__name__)

teams = [
    {"id": 1, "name": "Arsenal", "logo": "arsenal.png", "pj": 8, "pg": 8, "pe": 0, "pp": 0, "gf": 23, "ga": 4, "points": 24},
    {"id": 2, "name": "Bayern München", "logo": "bayern.png", "pj": 8, "pg": 7, "pe": 0, "pp": 1, "gf": 22, "ga": 8, "points": 21},
    {"id": 3, "name": "Liverpool", "logo": "liverpool.png", "pj": 8, "pg": 6, "pe": 0, "pp": 2, "gf": 20, "ga": 8, "points": 18},
    {"id": 4, "name": "Tottenham","logo": "tottenham.png", "pj": 8, "pg": 5, "pe": 2, "pp": 1, "gf": 17, "ga": 7, "points": 17},
    {"id": 5, "name": "Barcelona", "logo": "barcelona.png", "pj": 8, "pg": 5, "pe": 1, "pp": 2, "gf": 22, "ga": 14, "points": 16},
    {"id": 6, "name": "Chelsea", "logo": "chelsea.png", "pj": 8, "pg": 5, "pe": 1, "pp": 2, "gf": 17, "ga": 10, "points": 16},
    {"id": 7, "name": "Sporting CP", "logo": "sporting.png", "pj": 8, "pg": 5, "pe": 1, "pp": 2, "gf": 17, "ga": 11, "points": 16},
    {"id": 8, "name": "Manchester City", "logo": "city.png", "pj": 8, "pg": 5, "pe": 1, "pp": 2, "gf": 15, "ga": 9, "points": 16},
    {"id": 9, "name": "Real Madrid", "logo": "realmadrid.png", "pj": 8, "pg": 5, "pe": 0, "pp": 3, "gf": 21, "ga": 12, "points": 15},
    {"id": 10, "name": "Inter", "logo": "inter.png", "pj": 8, "pg": 5, "pe": 0, "pp": 3, "gf": 15, "ga": 7, "points": 15}
]

@app.route("/")
def home():
    sorted_teams = sorted(
        teams, 
        key=lambda team: (
            team["points"], 
            team["gf"] - team["ga"],
            team["gf"]
        ),
        reverse=True
    )
    return render_template("index.html", teams=sorted_teams)

@app.route("/team/<int:team_id>")
def team(team_id):
    for t in teams:
        if t["id"] == team_id:
            return render_template("team.html", team=t)
    
    return "Equipo no encontrado"

if __name__ == "__main__":
    app.run(debug=True)