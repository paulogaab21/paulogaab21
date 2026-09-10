# -*- coding: utf-8 -*-
"""Gera os SVGs do README de perfil em duas variantes: assets/ (claro) e assets/dark/ (escuro)."""
import io
import os

ROOT = r"C:\Users\Gabriel\projects\paulogaab21"

THEMES = {
    "light": {
        "INK": "#000000", "BONE": "#444444", "MUTED": "#888888", "DIM": "#999999",
        "RULE": "#C0C0C0", "GHOST": "#CCCCCC", "ACCENT": "#555555", "HAIR": "#E5E5E5",
    },
    "dark": {
        "INK": "#FFFFFF", "BONE": "#DDDDDD", "MUTED": "#777777", "DIM": "#666666",
        "RULE": "#444444", "GHOST": "#2A2A2A", "ACCENT": "#AAAAAA", "HAIR": "#1C1C1C",
    },
}

MONO = 'ui-monospace, "SFMono-Regular", "SF Mono", Menlo, Consolas, "Liberation Mono", monospace'

STYLE = """  <style>
    .mono { font-family: %s; }
    .draw { stroke: {RULE}; stroke-width: 1; stroke-dasharray: 1000; stroke-dashoffset: 1000; animation: d 1.4s cubic-bezier(.6,0,.2,1) .2s forwards; }
    @keyframes d { to { stroke-dashoffset: 0; } }
    .f { opacity: 0; animation: f .8s ease .1s forwards; }
    @keyframes f { to { opacity: 1; } }
    .rise { opacity: 0; animation: rise .7s cubic-bezier(.2,.7,.2,1) forwards; }
    @keyframes rise { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: translateY(0); } }
    .a1{animation-delay:.10s} .a2{animation-delay:.20s} .a3{animation-delay:.32s} .a4{animation-delay:.44s}
    .a5{animation-delay:.56s} .a6{animation-delay:.68s} .a7{animation-delay:.80s} .a8{animation-delay:.92s}
    .dot { animation: p 2.4s ease-in-out infinite; }
    @keyframes p { 0%%,100%% { opacity: 1 } 50%% { opacity: .35 } }
    .ring { animation: r 2.4s ease-out infinite; }
    @keyframes r { 0%% { transform: scale(.4); opacity: .8 } 80%%,100%% { transform: scale(2.6); opacity: 0 } }
    @media (prefers-reduced-motion: reduce) {
      .draw,.f,.rise,.dot,.ring { animation: none; }
      .draw { stroke-dashoffset: 0; } .f,.rise { opacity: 1; } .ring { opacity: 0; }
    }
  </style>
""" % MONO


def svg(name, w, h, label, body):
    return (
        '<svg viewBox="0 0 %d %d" width="%d" height="%d" fill="none" '
        'xmlns="http://www.w3.org/2000/svg" role="img" aria-label="%s">\n%s%s</svg>\n'
        % (w, h, w, h, label, STYLE, body)
    )


def txt(x, y, size, fill, s, cls="", ls=None, anchor=None):
    a = ' text-anchor="%s"' % anchor if anchor else ""
    l = ' letter-spacing="%s"' % ls if ls is not None else ""
    c = ' class="mono %s"' % cls if cls else ' class="mono"'
    return '  <text%s x="%s" y="%s" font-size="%s"%s fill="%s"%s>%s</text>\n' % (c, x, y, size, l, fill, a, s)


# ---------------------------------------------------------------- header
def header():
    b = ""
    b += txt(500, 40, 11, "{MUTED}", "PAULOGAAB21", "rise a1", ls=6, anchor="middle")
    b += txt(500, 112, 46, "{INK}", "PAULO GABRIEL", "rise a2", ls=4, anchor="middle")
    b += txt(500, 164, 46, "{INK}", "DA SILVA", "rise a3", ls=4, anchor="middle")
    b += '  <line class="draw" x1="340" y1="192" x2="660" y2="192" stroke-dasharray="320" stroke-dashoffset="320"/>\n'
    b += txt(500, 224, 13, "{MUTED}", "BACKEND / FULL STACK DEVELOPER · JUNDIA&#205;, BRAZIL", "rise a5", ls=3, anchor="middle")
    return svg("header-v1", 1000, 244, "Paulo Gabriel da Silva - backend and full stack developer", b)


# ---------------------------------------------------------------- sections
SECTIONS = [
    ("s01", "01", "WHOAMI", "~/01-whoami", 238, 833),
    ("s02", "02", "SYSTEM MAP", "~/02-system-map", 296, 799),
    ("s03", "03", "PROJECTS", "~/03-projects", 267, 816),
    ("s04", "04", "TELEMETRY", "~/04-telemetry", 282, 808),
    ("s05", "05", "THE ROUTE", "~/05-the-route", 282, 808),
    ("s06", "06", "STACK", "~/06-stack", 200, 842),
]


def section(num, label, path, x1, x2):
    b = '  <g class="f">\n'
    b += "  " + txt(48, 68, 52, "{GHOST}", num)
    b += "  " + txt(128, 58, 14, "{ACCENT}", label, ls=6)
    b += "  " + txt(952, 58, 11, "{MUTED}", path, ls=2, anchor="end")
    b += "  </g>\n"
    b += '  <line class="draw" x1="%d" y1="53" x2="%d" y2="53"/>\n' % (x1, x2)
    return svg("s", 1000, 92, "Section %s - %s" % (num, label), b)


# ---------------------------------------------------------------- whoami
def whoami():
    lines = [
        (32, 16, "{BONE}", "fourth-semester software engineering student, graduating september 2027.", "a1"),
        (60, 16, "{BONE}", "building across the full stack &#8212; Ruby on Rails &#183; Vue.js &#183; TypeScript &#183; PostgreSQL &#183; Docker.", "a2"),
        (92, 15, "{MUTED}", "off hours I go down to the metal: Xbox 360 PowerPC executables translated to C++", "a3"),
        (116, 15, "{MUTED}", "and recompiled to run natively on PC. no emulator in the middle.", "a4"),
        (148, 15, "{MUTED}", "before code, I supervised a store and its team at Drogasil &#8212; priorities, deadlines, people.", "a5"),
    ]
    b = ""
    for y, size, fill, s, a in lines:
        b += txt(48, y, size, fill, s, "rise " + a)
    b += '  <g class="f a6" style="transform-origin: 54px 186px">\n'
    b += '    <circle class="ring" cx="54" cy="186" r="5" fill="none" stroke="{ACCENT}" stroke-width="1" style="transform-origin: 54px 186px"/>\n'
    b += '    <circle class="dot" cx="54" cy="186" r="4" fill="{ACCENT}"/>\n'
    b += "  </g>\n"
    b += txt(76, 190, 12, "{BONE}", "OPEN TO JUNIOR ROLES", "rise a6", ls=3)
    return svg("whoami", 1000, 210, "whoami - bio, focus, status", b)


# ---------------------------------------------------------------- ecosystem
def ecosystem():
    nodes = [
        (96, 60, "IACoreX", "Rails &#183; Vue &#183; Sidekiq &#183; live", "a3"),
        (96, 240, "MiPaciente", "Rails &#183; Vue &#183; PostgreSQL", "a4"),
        (674, 60, "ufc3recomp", "C++ &#183; PowerPC &#8594; x86-64", "a5"),
        (674, 240, "NotiGO", "Go &#183; HTTP/JSON API", "a6"),
        (385, 14, "Fable2Recomp", "C++ &#183; contributor", "a6"),
        (385, 286, "reblue-ptbr-fix", "C++ &#183; 360 texture formats", "a7"),
    ]
    wires = [
        "M500 170 L211 82", "M500 170 L211 262", "M500 170 L789 82",
        "M500 170 L789 262", "M500 170 L500 36", "M500 170 L500 308",
    ]
    b = "  <g>\n"
    for d in wires:
        b += ('    <path class="draw" d="%s" stroke-dasharray="340" stroke-dashoffset="340"/>\n' % d)
    b += "  </g>\n"
    b += '  <g class="f a1">\n'
    b += '    <rect x="430" y="145" width="140" height="50" fill="none" stroke="{ACCENT}" stroke-width="1"/>\n'
    b += "  " + txt(500, 168, 11, "{INK}", "PAULOGAAB21", ls=3, anchor="middle")
    b += "  " + txt(500, 184, 10, "{MUTED}", "6 repositories", anchor="middle")
    b += "  </g>\n"
    for x, y, name, sub, a in nodes:
        b += '  <g class="f %s">\n' % a
        b += '    <rect x="%d" y="%d" width="230" height="44" fill="none" stroke="{RULE}"/>\n' % (x, y)
        b += "  " + txt(x + 14, y + 20, 12, "{BONE}", name)
        b += "  " + txt(x + 14, y + 35, 10, "{MUTED}", sub)
        b += "  </g>\n"
    return svg("ecosystem", 1000, 340, "Project ecosystem map", b)


# ---------------------------------------------------------------- projects
PROJECTS = [
    ("IACoreX", "iacorex.com",
     "Live AI-assisted customer support app &#8212; automated replies, scheduling,",
     "unified inbox and an analytics panel.",
     "RAILS &#183; PUMA &#183; SIDEKIQ &#183; POSTGRESQL &#183; VUE &#183; VITE &#183; TS"),
    ("MiPaciente", "mipaciente.com.br",
     "Clinical paperwork by link: intake forms, consent terms, contracts and",
     "progress notes.",
     "RAILS &#183; POSTGRESQL &#183; SIDEKIQ &#183; VUE &#183; VITE &#183; TS"),
    ("ufc3recomp", "v1.0.2",
     "Xbox 360&#8217;s UFC Undisputed 3 recompiled for PC. Not emulation: the PowerPC",
     "binary becomes C++ and compiles into a native .exe. Playable at 2K.",
     "C++ &#183; PYTHON &#183; CMAKE &#183; GHIDRA"),
    ("NotiGO", "academic",
     "HTTP/JSON API in Go that ingests events from seven services into one",
     "notification hub. Per-source idempotency, filtering, pagination, append-only.",
     "GO &#183; REST &#183; SOA &#183; JSONL"),
    ("reblue-ptbr-fix", "tool",
     "Installs the PT-BR Blue Dragon translation into re:Blue and kills the",
     "ACCESS_VIOLATION it caused, converting 27 textures to the 360 format.",
     "C++ &#183; TEXTURE FORMATS"),
    ("Fable2Recomp", "contributor",
     "Fable II ported to Windows and Linux through the same static recompilation",
     "route. Group effort, in progress.",
     "C++ &#183; REXGLUE SDK"),
]


def projects():
    b = ""
    y = 26
    for i, (name, meta, d1, d2, stack) in enumerate(PROJECTS):
        a = "a%d" % min(i + 1, 8)
        b += txt(48, y, 14, "{INK}", name, "rise " + a)
        b += txt(220, y, 14, "{BONE}", d1, "rise " + a)
        b += txt(952, y, 11, "{MUTED}", meta, "rise " + a, ls=2, anchor="end")
        b += txt(220, y + 20, 14, "{BONE}", d2, "rise " + a)
        b += txt(220, y + 42, 11, "{DIM}", stack, "rise " + a, ls=1)
        b += '  <line x1="48" y1="%d" x2="952" y2="%d" stroke="{HAIR}" stroke-width="1"/>\n' % (y + 58, y + 58)
        y += 80
    return svg("projects", 1000, y + 4, "Featured projects", b)


# ---------------------------------------------------------------- timeline
TIMELINE = [
    ("UNTIL MAR 2025", "Store supervisor &#8212; Drogasil",
     "Daily operations, team, priorities and customer service at a hard pace."),
    ("2024 &#8594;", "Software Engineering &#8212; Grupo Anchieta",
     "Fourth semester, expected to graduate in September 2027."),
    ("2025 &#8594;", "My own projects shipped",
     "IACoreX and MiPaciente deployed with Docker Compose, Nginx and PgBouncer."),
    ("NOW", "First job as a developer",
     "Backend or full stack, junior. Jundia&#237; area &#8212; on-site, hybrid or remote."),
]


def timeline():
    b = ""
    y = 26
    for i, (when, title, sub) in enumerate(TIMELINE):
        a = "a%d" % (i + 1)
        b += txt(48, y, 12, "{MUTED}", when, "rise " + a, ls=2)
        b += txt(210, y, 14, "{INK}", title, "rise " + a)
        b += txt(210, y + 20, 13, "{MUTED}", sub, "rise " + a)
        b += '  <line x1="48" y1="%d" x2="952" y2="%d" stroke="{HAIR}" stroke-width="1"/>\n' % (y + 38, y + 38)
        y += 62
    return svg("timeline", 1000, y + 4, "Timeline and experience", b)


# ---------------------------------------------------------------- stack
STACK = [
    ("LANGUAGES", "Ruby &#183; TypeScript &#183; JavaScript &#183; Go &#183; Python &#183; Java &#183; C++ &#183; SQL"),
    ("BACKEND", "Ruby on Rails &#183; Puma &#183; Sidekiq &#183; HTTP/JSON APIs &#183; REST &#183; SOA"),
    ("FRONTEND", "Vue.js &#183; Vite &#183; TypeScript &#183; componentization &#183; API consumption"),
    ("DATA", "PostgreSQL &#183; PgBouncer &#183; JSONL &#183; filtering, pagination, data modeling"),
    ("INFRA", "Docker &#183; Docker Compose &#183; Nginx &#183; Git &#183; GitHub &#183; per-environment deploys"),
    ("PRACTICES", "OpenAPI 3.1 &#183; tests &#183; CORS &#183; API key &#183; structured logs &#183; health checks"),
    ("LOW LEVEL", "Ghidra &#183; CMake &#183; PowerPC &#8594; x86-64 &#183; static recompilation"),
]


def stack():
    b = '  <line x1="178" y1="8" x2="178" y2="248" stroke="{RULE}" stroke-width="1" opacity=".4"/>\n'
    y = 30
    for i, (label, value) in enumerate(STACK):
        a = "a%d" % (i + 1)
        b += txt(48, y, 11, "{MUTED}", label, "rise " + a, ls=2)
        b += txt(196, y, 14, "{BONE}", value, "rise " + a)
        y += 34
    return svg("stack", 1000, 256, "Technical stack", b)


# ---------------------------------------------------------------- footer
def footer():
    b = '  <line class="draw" x1="48" y1="24" x2="952" y2="24"/>\n'
    b += '  <g style="transform-origin: 60px 64px">\n'
    b += '    <circle class="ring" cx="60" cy="64" r="5" fill="none" stroke="{ACCENT}" stroke-width="1" style="transform-origin: 60px 64px"/>\n'
    b += '    <circle class="dot" cx="60" cy="64" r="4" fill="{ACCENT}"/>\n'
    b += "  </g>\n"
    b += txt(82, 68, 12, "{BONE}", "STATUS &#8212; BUILDING", "f", ls=3)
    b += txt(952, 68, 12, "{MUTED}", "JUNDIA&#205;, BRAZIL &#183; github.com/paulogaab21", "f", ls=2, anchor="end")
    return svg("footer", 1000, 110, "Status: building. Jundiai, Brazil.", b)


# ---------------------------------------------------------------- write
def build():
    files = {"header-v1.svg": header(), "whoami.svg": whoami(), "ecosystem.svg": ecosystem(),
             "projects.svg": projects(), "timeline.svg": timeline(), "stack.svg": stack(),
             "footer.svg": footer()}
    for name, num, label, path, x1, x2 in SECTIONS:
        files[name + ".svg"] = section(num, label, path, x1, x2)

    for theme, palette in THEMES.items():
        outdir = os.path.join(ROOT, "assets") if theme == "light" else os.path.join(ROOT, "assets", "dark")
        if not os.path.isdir(outdir):
            os.makedirs(outdir)
        for name, content in files.items():
            s = content
            for k, v in palette.items():
                s = s.replace("{%s}" % k, v)
            io.open(os.path.join(outdir, name), "w", encoding="utf-8", newline="\n").write(s)

    print("wrote %d svg files x 2 themes into %s" % (len(files), ROOT))


if __name__ == "__main__":
    build()
