from flask import Flask, render_template

app = Flask(__name__)

teams = [
    {"id": 1, "name": "Real Madrid", "points": 12, "gf": 10, "ga": 4},
    {"id": 2, "name": "Bayern", "points": 10, "gf": 8, "ga": 3},
    {"id": 3, "name": "Arsenal", "points": 8, "gf": 7, "ga": 5},
    {"id": 4, "name": "Inter", "points": 6, "gf": 5, "ga": 6},
]

@app.route("/")
def home():
    return render_template("index.html", teams=teams)

@app.route("/team/<int:team_id>")
def team(team_id):
    for t in teams:
        if t["id"] == team_id:
            return render_template("team.html", team=t)
    
    return "Equipo no encontrado"

if __name__ == "__main__":
    app.run(debug=True)