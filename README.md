# Yalla Match Support

Official bilingual support website for the Yalla Match mobile app (يلا ماتش). It is a static site made with HTML, CSS, and JavaScript. It does not need Node.js, a build step, or a backend.

Arabic is the default language. English is available on every page. Legal pages describe only what is visible in the Flutter app and mark anything else for owner review.

## Technology

- HTML5 pages, one folder per route, so a refresh opens the real page
- CSS custom properties taken from the Flutter theme
- Tajawal, the app font, under the SIL Open Font License
- Vanilla JavaScript for the menu, language memory, FAQ filters, and the email draft form
- No React, npm, or server runtime

## Folder structure

```
yalla-match-support/
  index.html              Language entry. Sends visitors to /ar/ or their saved language.
  404.html
  favicon.ico
  robots.txt
  sitemap.xml
  ar/                     Arabic pages
  en/                     English pages
  assets/css              tokens.css and site.css
  assets/js               site-config.js and site.js
  assets/fonts            Tajawal and OFL.txt
  assets/images           App logo, icon, favicon, social image
  tools/build_site.py     Optional generator. The HTML is already generated.
  CONTENT_REVIEW.md       Verified facts and open legal questions
```

Each route is a real `index.html`:

| Page | Arabic | English |
| --- | --- | --- |
| Home | `ar/` | `en/` |
| FAQ | `ar/faq/` | `en/faq/` |
| Contact | `ar/contact/` | `en/contact/` |
| Privacy | `ar/privacy/` | `en/privacy/` |
| Terms | `ar/terms/` | `en/terms/` |
| Delete account | `ar/delete-account/` | `en/delete-account/` |

## Install

There is nothing to install.

## Run locally

From this folder:

```bash
python3 -m http.server 8080
```

Open `http://127.0.0.1:8080/`. The root page sends you to `ar/` unless English was saved earlier.

Do not open the HTML files with a `file://` address if you want the language redirect and directory URLs to behave like GitHub Pages.

## Production build

There is no production build. The files in this folder are the website.

If you change copy in `tools/build_site.py`, regenerate the pages:

```bash
python3 tools/build_site.py
```

You can also edit the HTML files directly. Running the generator again overwrites them.

## Deploy to GitHub Pages

Publish **only this folder** as its own repository. Do not turn on GitHub Pages for the Flutter app repository. That repository contains Firebase configuration and should not be served as a public website.

1. Create a new public GitHub repository for the support site.
2. Upload the contents of `yalla-match-support` so `index.html` is at the root of that repository. Do not upload the Flutter project.
3. In the repository, open Settings, then Pages.
4. Set the source to the branch you uploaded, folder `/ (root)`.
5. Wait until the Pages URL is shown.
6. Replace `YOUR_GITHUB_USERNAME` and `YOUR_REPOSITORY_NAME` in `sitemap.xml` and `robots.txt` with the real values.
7. Set `siteOrigin` in `assets/js/site-config.js` to the Pages URL without a trailing slash, for example `https://USERNAME.github.io/yalla-match-support`.

The project URL will look like:

```
https://USERNAME.github.io/REPOSITORY_NAME/
```

Relative links are used on purpose, so the same files work at that project path and at a custom domain.

## Base path

Do not hardcode the repository name in page links. Internal links are relative (`../en/faq/` and similar). If GitHub later serves the site from a project subpath, those links still resolve.

## Custom domain

1. In the Pages repository, add a file named `CNAME` that contains only the domain, for example `support.example.com`.
2. At the DNS host, point the domain at GitHub Pages using GitHub’s current custom-domain instructions.
3. Set `siteOrigin` in `assets/js/site-config.js` to `https://your-domain` with no trailing slash.
4. Replace the placeholder host in `sitemap.xml` and `robots.txt` with the same origin.

## Update Arabic content

Marketing and support copy for Arabic lives in `tools/build_site.py` (`render_home`, `FAQ`, `render_contact`, `render_privacy`, `render_terms`, `render_delete`). Keep the tone conversational for support pages and clear Modern Standard Arabic for privacy and terms. Then run:

```bash
python3 tools/build_site.py
```

## Update English content

English strings are in the same functions, in the `en` branches. Keep the same meaning as the Arabic page, especially for privacy, terms, and account deletion.

## Update contact information

Change the constants at the top of `tools/build_site.py`:

- `EMAIL`
- `WHATSAPP_URL`
- `WHATSAPP_DISPLAY`
- `FACEBOOK_URL`
- `LINKEDIN_URL`
- `PLAY_URL`

Regenerate the site. Do not copy the same address into individual components.

## Add the Apple App Store URL later

Leave `appStoreUrl` empty until Apple publishes the app.

In `assets/js/site-config.js`:

```javascript
window.YALLA_MATCH_SUPPORT = {
  siteOrigin: "https://USERNAME.github.io/REPOSITORY_NAME",
  appStoreUrl: "https://apps.apple.com/app/idXXXXXXXXX"
};
```

The download section shows App Store as coming soon. When `appStoreUrl` is an `https://apps.apple.com/...` link, the button becomes a real link. Do not point it at a guessed address.

## Update the privacy policy

Edit `render_privacy` in `tools/build_site.py`, regenerate, and read `CONTENT_REVIEW.md` before publishing. Do not add a “Last updated” date until the owner actually approves a revision. Remove or rewrite every “Needs confirmation” note only after that fact is confirmed.

The in-app policy is loaded from `GET api/policies`. If that service has the approved text, use that approved text here instead of inventing a replacement.

## Update the terms

Edit `render_terms` the same way. Do not add a subscription, refund policy, insurance promise, liability amount, or governing law until the owner and counsel confirm them.

## Maintain the account deletion page

The in-app path is Profile, Settings, Account, Delete Account. If those labels change in `assets/i18n`, update `render_delete` to match them.

The email button opens a draft to `support.yallamatch@gmail.com` with the subject `Yalla Match - Account Deletion Request`. It must never ask for a password or a one-time code.

An email request is not the same as the in-app deletion call (`DELETE api/users/me`). Say that clearly if the process changes.

## Publishing checklist

- Replace the sitemap and robots placeholder host.
- Set `siteOrigin`.
- Read `CONTENT_REVIEW.md` and approve privacy, terms, and deletion details.
- Confirm the Google Play URL still opens the Yalla Match listing.
- Add the App Store URL only after it exists.
