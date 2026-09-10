# -*- coding: utf-8 -*-
"""Gera assets/telemetry.svg e assets/activity.svg (claro e escuro) com dados
reais da API do GitHub.

Substitui os widgets de terceiros (github-readme-stats e
github-readme-activity-graph), que sao deploys no Vercel e saem do ar.

Token: usa TELEMETRY_TOKEN ou GITHUB_TOKEN do ambiente; sem nenhum dos dois,
cai para o `gh` da maquina.
"""
import io
import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_assets import ROOT, THEMES, STYLE, svg, txt  # noqa: E402

LOGIN = os.environ.get("GH_LOGIN", "paulogaab21")

QUERY = """
query($login:String!) {
  user(login:$login) {
    followers { totalCount }
    repositories(first:100, ownerAffiliations:OWNER, privacy:PUBLIC, isFork:false) {
      totalCount
      nodes {
        stargazerCount
        languages(first:10, orderBy:{field:SIZE, direction:DESC}) {
          edges { size node { name } }
        }
      }
    }
    contributionsCollection {
      totalCommitContributions
      totalPullRequestContributions
      contributionCalendar {
        totalContributions
        weeks { contributionDays { contributionCount } }
      }
    }
  }
}
"""


def fetch():
    token = os.environ.get("TELEMETRY_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if not token:
        # fora do CI, pega o token do gh ja autenticado
        token = subprocess.check_output(["gh", "auth", "token"]).decode("utf-8").strip()

    from urllib.request import Request, urlopen

    payload = json.dumps({"query": QUERY, "variables": {"login": LOGIN}}).encode("utf-8")
    req = Request("https://api.github.com/graphql", data=payload,
                  headers={"Authorization": "bearer " + token,
                           "Content-Type": "application/json",
                           "User-Agent": LOGIN + "-telemetry"})
    raw = urlopen(req, timeout=30).read().decode("utf-8")
    doc = json.loads(raw)
    if "errors" in doc:
        raise SystemExit("GraphQL: %s" % doc["errors"])
    return doc["data"]["user"]


def digest(user):
    repos = user["repositories"]
    contrib = user["contributionsCollection"]
    cal = contrib["contributionCalendar"]

    langs = {}
    for node in repos["nodes"]:
        for edge in node["languages"]["edges"]:
            langs[edge["node"]["name"]] = langs.get(edge["node"]["name"], 0) + edge["size"]
    total = sum(langs.values()) or 1
    top = sorted(langs.items(), key=lambda kv: -kv[1])[:5]

    # a grade guarda o dia a dia; o pico semanal so serve de rodape
    weeks = [[day["contributionCount"] for day in w["contributionDays"]] for w in cal["weeks"]]

    return {
        "stats": [
            ("public repositories", repos["totalCount"]),
            ("stars earned", sum(n["stargazerCount"] for n in repos["nodes"])),
            ("commits, last 12 months", contrib["totalCommitContributions"]),
            ("pull requests", contrib["totalPullRequestContributions"]),
            ("followers", user["followers"]["totalCount"]),
        ],
        "langs": [(name, 100.0 * size / total) for name, size in top],
        "weeks": weeks,
        "contributions": cal["totalContributions"],
    }


def telemetry_svg(data):
    b = '  <line x1="500" y1="18" x2="500" y2="196" stroke="{RULE}" stroke-width="1" opacity=".4"/>\n'
    b += txt(48, 24, 11, "{MUTED}", "STATS", "f", ls=3)
    y = 56
    for i, (label, value) in enumerate(data["stats"]):
        a = "a%d" % (i + 1)
        b += txt(48, y, 14, "{BONE}", label, "rise " + a)
        b += txt(452, y, 14, "{INK}", str(value), "rise " + a, anchor="end")
        y += 30

    b += txt(540, 24, 11, "{MUTED}", "LANGUAGES", "f", ls=3)
    y = 56
    for i, (name, pct) in enumerate(data["langs"]):
        a = "a%d" % (i + 1)
        b += txt(540, y, 14, "{BONE}", name, "rise " + a)
        b += txt(952, y, 12, "{DIM}", "%.1f%%" % pct, "rise " + a, anchor="end")
        b += '  <rect x="540" y="%d" width="412" height="3" fill="{HAIR}"/>\n' % (y + 8)
        b += ('  <rect class="rise %s" x="540" y="%d" width="%.1f" height="3" fill="{ACCENT}"/>\n'
              % (a, y + 8, max(2.0, 412.0 * pct / 100.0)))
        y += 30

    return svg("telemetry", 1000, 210, "GitHub statistics and language breakdown", b)


def activity_svg(data):
    """Grade de contribuicoes, 53 semanas x 7 dias.

    Area/linha nao serve aqui: contribuicao concentrada em poucas semanas vira
    uma reta com um pico e parece quebrada. A grade mostra o mesmo dado sem
    mentir sobre o volume.
    """
    weeks = data["weeks"]
    cell, gap = 12, 3
    pitch = cell + gap
    x0, y0 = 92, 48
    peak_day = max((max(w) for w in weeks if w), default=0)
    peak_week = max((sum(w) for w in weeks), default=0)

    # quatro faixas de intensidade sobre o pico do periodo
    def tone(count):
        if count <= 0:
            return "{HAIR}", 1.0
        if peak_day <= 1:
            return "{ACCENT}", 1.0
        ratio = count / float(peak_day)
        if ratio <= .25:
            return "{ACCENT}", .30
        if ratio <= .55:
            return "{ACCENT}", .55
        if ratio <= .80:
            return "{ACCENT}", .78
        return "{ACCENT}", 1.0

    b = txt(48, 24, 11, "{MUTED}", "CONTRIBUTION TELEMETRY", "f", ls=3)
    b += txt(952, 24, 11, "{DIM}", "%d contributions in the last year" % data["contributions"],
             "f", ls=1, anchor="end")

    for row, label in ((1, "mon"), (3, "wed"), (5, "fri")):
        b += txt(48, y0 + row * pitch + 9, 9, "{DIM}", label, "f", ls=1)

    for wi, week in enumerate(weeks):
        # cada semana entra logo depois da anterior: a grade preenche em onda
        delay = ".%02ds" % min(99, 6 + wi)
        for di, count in enumerate(week):
            fill, opacity = tone(count)
            b += ('  <rect class="f" style="animation-delay:%s" x="%d" y="%d" width="%d" height="%d" '
                  'rx="2" fill="%s" fill-opacity="%s"/>\n'
                  % (delay, x0 + wi * pitch, y0 + di * pitch, cell, cell, fill, opacity))

    legend_x = 952 - 4 * pitch - 74
    b += txt(legend_x - 8, y0 + 7 * pitch + 22, 9, "{DIM}", "less", "f", ls=1, anchor="end")
    for i, opacity in enumerate((1.0, .30, .55, .78, 1.0)):
        fill = "{HAIR}" if i == 0 else "{ACCENT}"
        b += ('  <rect class="f" x="%d" y="%d" width="9" height="9" rx="2" fill="%s" fill-opacity="%s"/>\n'
              % (legend_x + i * 13, y0 + 7 * pitch + 14, fill, opacity))
    b += txt(legend_x + 5 * 13 + 4, y0 + 7 * pitch + 22, 9, "{DIM}", "more", "f", ls=1)
    b += txt(48, y0 + 7 * pitch + 22, 10, "{DIM}", "peak %d in a week" % peak_week, "f", ls=2)

    return svg("activity", 1000, y0 + 7 * pitch + 44, "Contribution grid for the last year", b)


def main():
    data = digest(fetch())
    files = {"telemetry.svg": telemetry_svg(data), "activity.svg": activity_svg(data)}
    for theme, palette in THEMES.items():
        outdir = os.path.join(ROOT, "assets") if theme == "light" else os.path.join(ROOT, "assets", "dark")
        for name, content in files.items():
            s = content
            for key, value in palette.items():
                s = s.replace("{%s}" % key, value)
            io.open(os.path.join(outdir, name), "w", encoding="utf-8", newline="\n").write(s)
    print("telemetria: %d repos, %d stars, %d contribuicoes, pico %d/semana"
          % (data["stats"][0][1], data["stats"][1][1], data["contributions"],
             max(sum(w) for w in data["weeks"])))


if __name__ == "__main__":
    main()
