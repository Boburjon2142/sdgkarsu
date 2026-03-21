# Secure MVP Frontend

Next.js frontend for the Django REST backend.

## Security notes

- Uses browser `fetch` with `credentials: "include"` so the backend session stays in an HttpOnly cookie.
- No auth token is stored in `localStorage`.
- Private pages are guarded by a session check against `/api/auth/me/`.
- Only `NEXT_PUBLIC_API_BASE_URL` is exposed to the browser; no secrets belong in frontend env vars.

## Local setup

1. Copy `.env.example` to `.env.local`
2. Set `NEXT_PUBLIC_API_BASE_URL`
3. Run `npm install`
4. Run `npm run dev`
