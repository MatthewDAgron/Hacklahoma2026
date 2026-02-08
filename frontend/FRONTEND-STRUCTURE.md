# Frontend folder structure

Use this layout so the UI lives next to Django without changing your code.

```
frontend/
├── manage.py                 # Django
├── db.sqlite3
├── django_project/           # Django backend (settings, urls, wsgi)
│   ├── settings.py
│   ├── urls.py
│   └── ...
└── ui/                       # Next.js app (formerly launch-ui-main)
    ├── app/                  # Next app router pages
    │   ├── layout.tsx
    │   ├── page.tsx
    │   └── globals.css
    ├── components/
    │   ├── contexts/
    │   ├── logos/
    │   ├── sections/
    │   └── ui/
    ├── config/
    ├── lib/
    ├── public/
    ├── styles/
    ├── package.json
    ├── next.config.mjs
    └── tsconfig.json
```

- **Django:** run from `frontend/` with `python manage.py runserver`.
- **UI (Next.js):** run from `frontend/ui/` with `npm install` then `npm run dev`.

No code was changed; only `launch-ui-main` was renamed to `ui`.
