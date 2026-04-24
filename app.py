from flask import Flask, render_template, request
import json

app = Flask(__name__)

def load_teams():
    with open("teams.json", encoding="utf-8") as f:
        return json.load(f)

def get_team_logos():
    teams = load_teams()
    return {team["name"]: team["logo"] for team in teams}

def generate_semifinals(data):
    quarterfinals = data["quarterfinals"]

    data["semifinals"][0]["team1"] = quarterfinals[0]["winner"]
    data["semifinals"][0]["team2"] = quarterfinals[1]["winner"]

    data["semifinals"][1]["team1"] = quarterfinals[2]["winner"]
    data["semifinals"][1]["team2"] = quarterfinals[3]["winner"]

    return data

def generate_final(data):
    semifinals = data["semifinals"]

    data["final"][0]["team1"] = semifinals[0]["winner"]
    data["final"][0]["team2"] = semifinals[1]["winner"]

    return data

def get_team_ids():
    teams = load_teams()
    return {team["name"]: team["id"] for team in teams}

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

def load_knockout():
    with open("knockout.json", encoding="utf-8") as f:
        return json.load(f)

@app.route("/knockout")
def knockout():
    data = load_knockout()

    data = generate_semifinals(data)
    data = generate_final(data)

    team_logos = get_team_logos()
    team_ids = get_team_ids()

    for round_matches in data.values():
        for match in round_matches:
            if match.get("team1"):
                match["logo1"] = team_logos.get(match["team1"], "default.png")
                match["id1"] = team_ids.get(match["team1"])

            if match.get("team2"):
                match["logo2"] = team_logos.get(match["team2"], "default.png")
                match["id2"] = team_ids.get(match["team2"])

    return render_template("knockout.html", data=data)

if __name__ == "__main__":
    app.run(debug=True)