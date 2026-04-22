from flask import Flask, render_template, request
import json

app = Flask(__name__)

def load_teams():
    with open("teams.json", encoding="utf-8") as f:
        return json.load(f)

@app.route("/")
def home():
    teams = load_teams()

    query = request.args.get("q")

    if query:
        teams = [team for team in teams if query.lower() in team["name"].lower()]

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
    teams = load_teams()

    for t in teams:
        if t["id"] == team_id:
            return render_template("team.html", team=t)
    
    return "Equipo no encontrado"

if __name__ == "__main__":
    app.run(debug=True)