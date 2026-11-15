# Visuale — сайт (GitHub Pages)

Публичные страницы для App Store Connect: политика конфиденциальности, условия использования, поддержка (EN — корень, RU — `/ru/`, ES — `/es/`).

Тексты берутся из `Visuale/docs/*.md` (рядом с сайтом или в `~/Projects/Visuale`; другой путь — переменная `VISUALE_DOCS`). После правки документов:

```
python3 build.py
git commit -am "Обновить юридические тексты" && git push
```
