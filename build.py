#!/usr/bin/env python3
"""Сборка статического сайта Visuale для GitHub Pages из юридических текстов
в ../Visuale/docs. Запуск: python3 build.py (после правки docs/*.md в Visuale)."""
import html, pathlib, markdown

ROOT = pathlib.Path(__file__).parent
DOCS = ROOT.parent / "Visuale" / "docs"
SUPPORT = "support@visualeapp.com"

T = {
    "en": dict(lang="en", other="ru", other_label="Русский", home="Home", privacy="Privacy Policy",
               terms="Terms of Use", support="Support", tagline="Learn Spanish vocabulary with illustrated flashcards.",
               home_text="Visuale is an iPhone app for learning Spanish vocabulary (Spanish as spoken in Spain) with illustrated flashcards, spaced repetition, exercises and photo scanning.",
               support_title="Support",
               support_text=f"Questions, bug reports or ideas? Write to <a href=\"mailto:{SUPPORT}\">{SUPPORT}</a> — we usually reply within a few days.",
               support_more="Other contacts: <a href=\"mailto:privacy@visualeapp.com\">privacy@visualeapp.com</a> (personal data), <a href=\"mailto:legal@visualeapp.com\">legal@visualeapp.com</a> (legal matters, copyright), <a href=\"mailto:ideas@visualeapp.com\">ideas@visualeapp.com</a> (ideas), <a href=\"mailto:sales@visualeapp.com\">sales@visualeapp.com</a> (cooperation).",
               faq=[("Is Visuale free?", "Yes. Visuale is in early access: all features are free right now. We will announce any change in advance."),
                    ("Do I need an account?", "No. Your decks and progress sync between your devices through your own iCloud account."),
                    ("My cards don't sync.", "Check that you are signed in to iCloud on both devices and that iCloud is enabled for Visuale in Settings → your name → iCloud."),
                    ("How do I delete my data?", "Delete the app and, if needed, its iCloud data in Settings → your name → iCloud → Manage Account Storage → Visuale.")]),
    "ru": dict(lang="ru", other="en", other_label="English", home="Главная", privacy="Политика конфиденциальности",
               terms="Условия использования", support="Поддержка", tagline="Испанские слова по иллюстрированным карточкам.",
               home_text="Visuale — приложение для iPhone для изучения испанской лексики (испанский Испании): иллюстрированные карточки, интервальное повторение, упражнения и сканирование фото.",
               support_title="Поддержка",
               support_text=f"Вопросы, ошибки или идеи? Пишите на <a href=\"mailto:{SUPPORT}\">{SUPPORT}</a> — обычно отвечаем в течение нескольких дней.",
               support_more="Другие адреса: <a href=\"mailto:privacy@visualeapp.com\">privacy@visualeapp.com</a> (персональные данные), <a href=\"mailto:legal@visualeapp.com\">legal@visualeapp.com</a> (юридические вопросы, авторское право), <a href=\"mailto:ideas@visualeapp.com\">ideas@visualeapp.com</a> (идеи), <a href=\"mailto:sales@visualeapp.com\">sales@visualeapp.com</a> (сотрудничество).",
               faq=[("Visuale бесплатный?", "Да. Сейчас идёт ранний доступ: все функции бесплатны. Об изменениях мы сообщим заранее."),
                    ("Нужна ли регистрация?", "Нет. Колоды и прогресс синхронизируются между вашими устройствами через ваш собственный iCloud."),
                    ("Карточки не синхронизируются.", "Проверьте, что на обоих устройствах выполнен вход в iCloud и что для Visuale включён iCloud: Настройки → ваше имя → iCloud."),
                    ("Как удалить мои данные?", "Удалите приложение и при необходимости его данные в iCloud: Настройки → ваше имя → iCloud → Управлять хранилищем → Visuale.")]),
}

CSS = """
:root{--bg:#fbfaf7;--fg:#1d1d1f;--muted:#6e6e73;--line:#e5e2dc;--card:#ffffff;--accent:#5b5f97}
@media (prefers-color-scheme:dark){:root{--bg:#141416;--fg:#f2f2f4;--muted:#a1a1a6;--line:#2c2c30;--card:#1c1c1f;--accent:#a5a8e6}}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--fg);font:17px/1.6 -apple-system,BlinkMacSystemFont,"SF Pro Text","Segoe UI",Roboto,sans-serif}
header,main,footer{max-width:760px;margin:0 auto;padding:0 20px}
header{display:flex;flex-wrap:wrap;gap:8px 18px;align-items:center;padding-top:22px;padding-bottom:14px;border-bottom:1px solid var(--line)}
header .brand{font-weight:700;font-size:19px;color:var(--fg);text-decoration:none;margin-right:auto;display:flex;align-items:center;gap:10px}
header .brand img{width:32px;height:32px;border-radius:8px}
header nav{display:flex;flex-wrap:wrap;gap:6px 16px;font-size:15px}
a{color:var(--accent)}header nav a{text-decoration:none}header nav a[aria-current]{color:var(--fg);font-weight:600}
main{padding-top:26px;padding-bottom:40px}
h1{font-size:30px;line-height:1.2;margin:.2em 0 .6em}h2{font-size:21px;margin:1.8em 0 .5em}h3{font-size:18px;margin:1.4em 0 .4em}
hr{border:0;border-top:1px solid var(--line);margin:2em 0}
blockquote{margin:1.2em 0;padding:12px 16px;background:var(--card);border:1px solid var(--line);border-radius:12px}
blockquote p{margin:.3em 0}code{font:15px ui-monospace,SFMono-Regular,Menlo,monospace;background:var(--card);border:1px solid var(--line);border-radius:6px;padding:1px 5px;overflow-wrap:anywhere}
ul{padding-left:1.3em}li{margin:.3em 0}
.lead{font-size:19px;color:var(--muted)}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px;margin-top:22px}
.cards a{display:block;padding:16px;background:var(--card);border:1px solid var(--line);border-radius:14px;text-decoration:none;color:var(--fg);font-weight:600}
dt{font-weight:600;margin-top:1em}dd{margin:.2em 0 0}
footer{padding-top:16px;padding-bottom:30px;border-top:1px solid var(--line);color:var(--muted);font-size:14px}
"""

def page(lang, key, title, body, depth):
    t = T[lang]
    up = "../" * depth
    prefix = "" if lang == "en" else "ru/"
    other_prefix = "ru/" if lang == "en" else ""
    paths = {"home": "", "privacy": "privacy/", "terms": "terms/", "support": "support/"}
    nav = "".join(
        f'<a href="{up}{prefix}{p}"' + (' aria-current="page"' if k == key else "") + f">{html.escape(t[k])}</a>"
        for k, p in paths.items() if k != "home")
    nav += f' <a href="{up}{other_prefix}{paths[key]}" hreflang="{t["other"]}" lang="{t["other"]}">{t["other_label"]}</a>'
    return f"""<!doctype html>
<html lang="{lang}"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)} — Visuale</title>
<meta name="description" content="{html.escape(t['tagline'])}">
<link rel="icon" href="{up}icon.png"><style>{CSS}</style></head>
<body><header><a class="brand" href="{up}{prefix}"><img src="{up}icon.png" alt="">Visuale</a><nav>{nav}</nav></header>
<main>{body}</main>
<footer>© 2026 Aleksei Vasilev · <a href="mailto:{SUPPORT}">{SUPPORT}</a></footer></body></html>
"""

def write(rel, text):
    p = ROOT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")

def md(name):
    src = (DOCS / name).read_text(encoding="utf-8")
    return markdown.markdown(src, extensions=["extra", "sane_lists", "nl2br"])

for lang in ("en", "ru"):
    t = T[lang]; base = "" if lang == "en" else "ru/"; d0 = 0 if lang == "en" else 1
    home = (f"<h1>Visuale</h1><p class=\"lead\">{t['tagline']}</p><p>{t['home_text']}</p>"
            f"<div class=\"cards\"><a href=\"privacy/\">{t['privacy']}</a><a href=\"terms/\">{t['terms']}</a><a href=\"support/\">{t['support']}</a></div>")
    write(f"{base}index.html", page(lang, "home", "Visuale", home, d0))
    write(f"{base}privacy/index.html", page(lang, "privacy", t["privacy"], f"<h1>{t['privacy']}</h1>" + md(f"privacy-policy-{lang}.md"), d0 + 1))
    write(f"{base}terms/index.html", page(lang, "terms", t["terms"], f"<h1>{t['terms']}</h1>" + md(f"terms-of-use-{lang}.md"), d0 + 1))
    faq = "".join(f"<dt>{html.escape(q)}</dt><dd>{html.escape(a)}</dd>" for q, a in t["faq"])
    sup = f"<h1>{t['support_title']}</h1><p class=\"lead\">{t['support_text']}</p><dl>{faq}</dl><p>{t['support_more']}</p>"
    write(f"{base}support/index.html", page(lang, "support", t["support"], sup, d0 + 1))
print("built")
