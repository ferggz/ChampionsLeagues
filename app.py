from flask import Flask, render_template, request, abort
import json

app = Flask(__name__)


def load_json(filename):
    with open(filename, encoding="utf-8") as f:
        return json.load(f)


def load_teams():
    return load_json("teams.json")


def load_knockout():
    return load_json("knockout.json")


def sort_teams(teams):
    return sorted(
        teams,
        key=lambda team: (
            team["points"],
            team["gf"] - team["ga"],
            team["gf"]
        ),
        reverse=True
    )


def get_team_by_id(team_id):
    teams = load_teams()
    return next((team for team in teams if team["id"] == team_id), None)


def get_team_data():
    teams = load_teams()
    logos = {team["name"]: team["logo"] for team in teams}
    ids = {team["name"]: team["id"] for team in teams}

    return logos, ids


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


def enrich_knockout_data(data):
    data = generate_semifinals(data)
    data = generate_final(data)

    team_logos, team_ids = get_team_data()

    for round_matches in data.values():
        for match in round_matches:
            if match.get("team1"):
                match["logo1"] = team_logos.get(match["team1"], "default.png")
                match["id1"] = team_ids.get(match["team1"])

            if match.get("team2"):
                match["logo2"] = team_logos.get(match["team2"], "default.png")
                match["id2"] = team_ids.get(match["team2"])

    return data


@app.route("/")
def home():
    teams = load_teams()

    query = request.args.get("q")

    if query:
        teams = [
            team for team in teams
            if query.lower() in team["name"].lower()
        ]

    sorted_teams = sort_teams(teams)

    return render_template("index.html", teams=sorted_teams)


@app.route("/team/<int:team_id>")
def team(team_id):
    selected_team = get_team_by_id(team_id)

    if selected_team is None:
        abort(404)

    return render_template("team.html", team=selected_team)


@app.route("/knockout")
def knockout():
    data = load_knockout()
    data = enrich_knockout_data(data)

    return render_template("knockout.html", data=data)


@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True)