#!/usr/bin/env python3
"""Generate the static Yalla Match support website. No packages required."""

from html import escape
from pathlib import Path
from urllib.parse import quote
import struct

ROOT = Path(__file__).resolve().parents[1]
EMAIL = "support.yallamatch@gmail.com"
WHATSAPP_URL = "https://wa.me/201019260479"
WHATSAPP_DISPLAY = "+20 101 926 0479"
FACEBOOK_URL = "https://www.facebook.com/profile.php?id=61593627575914"
LINKEDIN_URL = "https://www.linkedin.com/in/akram-mousa-29a83b206/"
PLAY_URL = "https://play.google.com/store/apps/details?id=com.akram.yallamatch.app&hl=ar"
SITE_PLACEHOLDER = "https://YOUR_GITHUB_USERNAME.github.io/YOUR_REPOSITORY_NAME"

PAGES = [
    ("home", {"ar": "الرئيسية", "en": "Home"}, ""),
    ("faq", {"ar": "الأسئلة الشائعة", "en": "FAQ"}, "faq/"),
    ("contact", {"ar": "تواصل معنا", "en": "Contact"}, "contact/"),
    ("privacy", {"ar": "الخصوصية", "en": "Privacy"}, "privacy/"),
    ("terms", {"ar": "الشروط", "en": "Terms"}, "terms/"),
    ("delete", {"ar": "حذف الحساب", "en": "Delete Account"}, "delete-account/"),
]

FOOTER_LABELS = {
    "home": {"ar": "الرئيسية", "en": "Home"},
    "faq": {"ar": "الأسئلة الشائعة", "en": "FAQ"},
    "contact": {"ar": "تواصل معنا", "en": "Contact"},
    "privacy": {"ar": "سياسة الخصوصية", "en": "Privacy Policy"},
    "terms": {"ar": "الشروط والأحكام", "en": "Terms & Conditions"},
    "delete": {"ar": "حذف الحساب", "en": "Delete Account"},
}

DELETE_BODY = """Hello Yalla Match Support,

I request deletion of my Yalla Match account and the associated data.

Google account email used in the app:
Extra details:

Please do not send a password, OTP, or any other authentication secret.

مرحباً فريق دعم يلا ماتش،

أطلب حذف حسابي في يلا ماتش والبيانات المرتبطة به.

البريد الإلكتروني لحساب Google المستخدم في التطبيق:
تفاصيل إضافية:

لا ترسل كلمة المرور أو رمز التحقق أو أي بيانات دخول سرية.
"""

DELETE_MAILTO = (
    f"mailto:{EMAIL}?subject={quote('Yalla Match - Account Deletion Request')}"
    f"&body={quote(DELETE_BODY)}"
)


def esc(value):
    return escape(str(value), quote=True)


def prefix_for(path):
    extra = len([part for part in path.split("/") if part])
    return "../" * (1 + extra)


def page_href(from_path, lang, to_path):
    return f"{prefix_for(from_path)}{lang}/{to_path}"


def asset(from_path, relative):
    return prefix_for(from_path) + relative


ICONS = {
    "faq": '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M9.5 9a2.5 2.5 0 1 1 3.5 2.3c-.8.4-1.2.9-1.2 1.7V14"/><path d="M12 17h.01"/></svg>',
    "mail": '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M4 7l8 6 8-6"/></svg>',
    "shield": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3l7 3v6c0 4.5-2.8 7.6-7 9-4.2-1.4-7-4.5-7-9V6l7-3z"/><path d="M9 12l2 2 4-4"/></svg>',
    "trash": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 7h16"/><path d="M9 7V5h6v2"/><path d="M7 7l1 13h8l1-13"/></svg>',
    "search": '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="6"/><path d="M16 16l4 4"/></svg>',
    "users": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M16 20v-1.5a3.5 3.5 0 0 0-3.5-3.5h-5A3.5 3.5 0 0 0 4 18.5V20"/><circle cx="10" cy="8" r="3"/><path d="M20 20v-1.5a3.2 3.2 0 0 0-2.4-3.1"/><path d="M16 5.2a3 3 0 0 1 0 5.6"/></svg>',
    "play": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M8 6l10 6-10 6V6z"/></svg>',
    "chat": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 17l-2 3V6a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2H6z"/></svg>',
    "pin": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 21s6-5.2 6-10a6 6 0 1 0-12 0c0 4.8 6 10 6 10z"/><circle cx="12" cy="11" r="2"/></svg>',
}


def icon(name):
    return f'<span class="icon-badge">{ICONS[name]}</span>'


def external(href, label, class_name=""):
    class_attr = f' class="{class_name}"' if class_name else ""
    return (
        f'<a href="{esc(href)}" target="_blank" rel="noopener noreferrer"{class_attr}>'
        f"{esc(label)}</a>"
    )


def layout(lang, page_id, path, title, description, body):
    direction = "rtl" if lang == "ar" else "ltr"
    other = "en" if lang == "ar" else "ar"
    home_href = page_href(path, lang, "")
    other_href = page_href(path, other, path)
    nav_items = []
    for item_id, labels, item_path in PAGES:
        current = ' aria-current="page"' if item_id == page_id else ""
        href = page_href(path, lang, item_path)
        nav_items.append(
            f'<li><a href="{esc(href)}"{current}>{esc(labels[lang])}</a></li>'
        )
    footer_items = []
    for item_id, _labels, item_path in PAGES:
        href = page_href(path, lang, item_path)
        footer_items.append(
            f'<li><a href="{esc(href)}">{esc(FOOTER_LABELS[item_id][lang])}</a></li>'
        )
    menu_label = "القائمة" if lang == "ar" else "Menu"
    skip_label = "تخطي إلى المحتوى" if lang == "ar" else "Skip to content"
    brand_alt = "يلا ماتش" if lang == "ar" else "Yalla Match"
    footer_tagline = (
        "يلا ماتش — العب أكتر، ودوّر أقل."
        if lang == "ar"
        else "Yalla Match — Less Searching, More Playing."
    )
    rights = "جميع الحقوق محفوظة." if lang == "ar" else "All rights reserved."
    lang_name = {"ar": "العربية", "en": "English"}
    canonical = "./"
    xdefault = "./" if lang == "ar" else page_href(path, "ar", path)
    image = asset(path, "assets/images/og-image.png")
    css = asset(path, "assets/css/site.css")
    config = asset(path, "assets/js/site-config.js")
    script = asset(path, "assets/js/site.js")
    logo = asset(path, "assets/images/logo-horizontal.png")
    logo_white = asset(path, "assets/images/logo-horizontal-white.png")
    favicon = asset(path, "assets/images/favicon-32.png")
    apple = asset(path, "assets/images/apple-touch-icon.png")
    return f"""<!DOCTYPE html>
<html lang="{lang}" dir="{direction}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(description)}">
  <link rel="canonical" href="{canonical}">
  <link rel="alternate" hreflang="ar" href="{('./' if lang == 'ar' else page_href(path, 'ar', path))}">
  <link rel="alternate" hreflang="en" href="{('./' if lang == 'en' else page_href(path, 'en', path))}">
  <link rel="alternate" hreflang="x-default" href="{xdefault}">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{esc(title)}">
  <meta property="og:description" content="{esc(description)}">
  <meta property="og:locale" content="{'ar_EG' if lang == 'ar' else 'en_US'}">
  <meta property="og:locale:alternate" content="{'en_US' if lang == 'ar' else 'ar_EG'}">
  <meta property="og:image" content="{image}">
  <meta property="og:url" content="{canonical}">
  <meta name="twitter:card" content="summary">
  <meta name="twitter:title" content="{esc(title)}">
  <meta name="twitter:description" content="{esc(description)}">
  <meta name="twitter:image" content="{image}">
  <meta name="theme-color" content="#01234D">
  <link rel="icon" type="image/png" href="{favicon}">
  <link rel="apple-touch-icon" href="{apple}">
  <link rel="stylesheet" href="{css}">
</head>
<body>
  <a class="skip-link" href="#content">{skip_label}</a>
  <header class="site-header">
    <div class="header-inner">
      <a class="brand" href="{esc(home_href)}">
        <img src="{logo}" alt="{esc(brand_alt)}" width="168" height="40">
      </a>
      <div class="header-tools">
        <nav class="lang-switch" aria-label="{'اللغة' if lang == 'ar' else 'Language'}">
          <a href="{esc(page_href(path, 'ar', path))}" data-lang-link="ar" hreflang="ar" lang="ar"{' aria-current="true"' if lang == 'ar' else ''}>العربية</a>
          <a href="{esc(page_href(path, 'en', path))}" data-lang-link="en" hreflang="en" lang="en"{' aria-current="true"' if lang == 'en' else ''}>English</a>
        </nav>
        <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav">
          <span class="visually-hidden" style="position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)">{esc(menu_label)}</span>
          <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
        </button>
      </div>
      <nav id="site-nav" class="site-nav" aria-label="{esc(menu_label)}">
        <ul>
          {''.join(nav_items)}
        </ul>
      </nav>
    </div>
  </header>
  <main id="content" class="main">
    {body}
  </main>
  <footer class="site-footer">
    <div class="footer-inner">
      <div class="footer-grid">
        <div class="footer-brand">
          <img src="{logo_white}" alt="{esc(brand_alt)}" width="190" height="42">
          <p>{esc(footer_tagline)}</p>
        </div>
        <div>
          <ul class="footer-links">{''.join(footer_items)}</ul>
        </div>
        <div>
          <ul class="footer-links">
            <li><a class="ltr" href="mailto:{EMAIL}">{EMAIL}</a></li>
            <li>{external(WHATSAPP_URL, 'WhatsApp')}</li>
            <li>{external(FACEBOOK_URL, 'Facebook')}</li>
            <li>{external(LINKEDIN_URL, 'LinkedIn')}</li>
          </ul>
        </div>
      </div>
      <p class="footer-bottom">© <span id="copyright-year">2026</span> Yalla Match. {esc(rights)}</p>
    </div>
  </footer>
  <script src="{config}"></script>
  <script src="{script}"></script>
</body>
</html>
"""


def hero_actions(lang, path):
    if lang == "ar":
        primary = "تواصل مع الدعم"
        secondary = "الأسئلة الشائعة"
    else:
        primary = "Contact Support"
        secondary = "Frequently Asked Questions"
    return f"""
      <div class="hero-actions">
        <a class="button button-primary" href="{esc(page_href(path, lang, 'contact/'))}">{esc(primary)}</a>
        <a class="button button-secondary" href="{esc(page_href(path, lang, 'faq/'))}">{esc(secondary)}</a>
      </div>
    """


def render_home(lang, path):
    icon_src = asset(path, "assets/images/app-icon.png")
    if lang == "ar":
        heading = "أهلًا بيك في مركز دعم يلا ماتش"
        description = "محتاج مساعدة في استخدام يلا ماتش؟ هنا هتلاقي إجابات لأهم الأسئلة، وطرق التواصل مع فريق الدعم، وكل المعلومات اللي تساعدك تستمتع بتجربة لعب أسهل."
        cards = [
            ("faq/", "faq", "الأسئلة الشائعة", "إجابات سريعة عن التسجيل، إنشاء المباريات، والانضمام إليها."),
            ("contact/", "mail", "تواصل معنا", "محتاج مساعدة؟ تواصل مع فريق الدعم من خلال البريد الإلكتروني أو واتساب."),
            ("privacy/", "shield", "الخصوصية والأمان", "اعرف المزيد عن كيفية التعامل مع بياناتك وخصوصيتك."),
            ("delete-account/", "trash", "حذف الحساب", "اعرف خطوات طلب حذف حسابك والبيانات المرتبطة به."),
        ]
        steps = [
            ("اكتشف ماتش", "تصفح المباريات القريبة منك واختار اللي يناسبك."),
            ("انضم أو نظّم", "انضم لماتش متاح أو أنشئ ماتشك بنفسك."),
            ("يلا نلعب!", "تواصل مع اللاعبين واستعد لمباراتك الجاية."),
        ]
        how = "يلا ماتش بيشتغل إزاي؟"
        download_title = "لسه منزلتش يلا ماتش؟"
        download_text = "التطبيق متاح على Google Play. نسخة App Store لسه مش متاحة."
        play_small = "متوفر على"
        play_name = "Google Play"
        soon_small = "قريباً"
        soon_name = "App Store"
        soon_hint = "تنزيل"
    else:
        heading = "Welcome to Yalla Match Support"
        description = "Need help using Yalla Match? Find answers to common questions, get assistance, and explore helpful information to make your sports experience easier."
        cards = [
            ("faq/", "faq", "Frequently Asked Questions", "Quick answers about registration, creating matches, and joining games."),
            ("contact/", "mail", "Contact Us", "Need assistance? Reach our support team by email or WhatsApp."),
            ("privacy/", "shield", "Privacy & Safety", "Learn more about how your information and privacy are handled."),
            ("delete-account/", "trash", "Delete Account", "Learn how to request deletion of your account and associated data."),
        ]
        steps = [
            ("Find a Match", "Explore nearby games and choose the one that suits you."),
            ("Join or Organize", "Join an available match or create your own."),
            ("Let's Play!", "Connect with players and get ready for your next game."),
        ]
        how = "How Yalla Match Works"
        download_title = "Haven't Downloaded Yalla Match Yet?"
        download_text = "The app is available on Google Play. The App Store version is not available yet."
        play_small = "Get it on"
        play_name = "Google Play"
        soon_small = "Coming soon"
        soon_name = "App Store"
        soon_hint = "Download"
    card_html = []
    for href, icon_name, title, text in cards:
        card_html.append(
            f'<a class="support-card" href="{esc(page_href(path, lang, href))}">{icon(icon_name)}<h3>{esc(title)}</h3><p>{esc(text)}</p></a>'
        )
    step_html = []
    for index, (title, text) in enumerate(steps, start=1):
        step_html.append(
            f'<article class="step-card"><span class="step-number">{index}</span><h3>{esc(title)}</h3><p>{esc(text)}</p></article>'
        )
    quick = "اختصارات الدعم" if lang == "ar" else "Support shortcuts"
    schema_name = "مركز دعم يلا ماتش" if lang == "ar" else "Yalla Match Support"
    return f"""
    <section class="section hero">
      <img class="hero-mark" src="{icon_src}" alt="" width="88" height="88">
      <h1>{esc(heading)}</h1>
      <p>{esc(description)}</p>
      {hero_actions(lang, path)}
    </section>
    <section class="section" aria-labelledby="quick-support">
      <div class="section-heading"><h2 id="quick-support">{esc(quick)}</h2></div>
      <div class="card-grid">{''.join(card_html)}</div>
    </section>
    <section class="section" aria-labelledby="how-it-works">
      <div class="section-heading"><h2 id="how-it-works">{esc(how)}</h2></div>
      <div class="steps">{''.join(step_html)}</div>
    </section>
    <section class="section" aria-labelledby="download-title">
      <div class="download-band">
        <img src="{icon_src}" alt="" width="72" height="72">
        <div>
          <h2 id="download-title">{esc(download_title)}</h2>
          <p>{esc(download_text)}</p>
          <div class="store-row">
            <a class="store-badge" href="{esc(PLAY_URL)}" target="_blank" rel="noopener noreferrer">
              {ICONS['play']}
              <span class="store-copy"><small>{esc(play_small)}</small><span>{esc(play_name)}</span></span>
            </a>
            <div id="app-store-slot" data-hint="{esc(soon_hint)}">
              <span class="store-badge is-static" aria-disabled="true">
                {ICONS['play']}
                <span class="store-copy"><small>{esc(soon_small)}</small><span>{esc(soon_name)}</span></span>
              </span>
            </div>
          </div>
        </div>
      </div>
    </section>
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "WebSite",
      "name": "{schema_name}",
      "inLanguage": "{lang}",
      "publisher": {{
        "@type": "Organization",
        "name": "Yalla Match",
        "email": "{EMAIL}"
      }}
    }}
    </script>
    """


FAQ = {
    "ar": [
        ("start", "إيه هو تطبيق يلا ماتش؟", "يلا ماتش تطبيق بيساعدك تلاقي مباريات رياضية، وتنضم للماتشات المتاحة، أو تنظم مباراة بنفسك وتوصل للاعبين مهتمين بالمشاركة. الرياضات الظاهرة في التطبيق بتعتمد على القائمة الراجعة من الخدمة."),
        ("matches", "إزاي ألاقي ماتش قريب مني؟", "من الرئيسية تقدر تتصفح المباريات وتفلترها حسب الرياضة، وحسب المحافظة أو المدينة أو القرية، وبعدين تفتح تفاصيل الماتش. التطبيق مش بيطلب إذن موقع الجهاز. لو ظهرت مسافة، بتكون جاية من بيانات المباراة نفسها."),
        ("matches", "إزاي أنضم لماتش؟", "اختار المباراة المناسبة، وراجع تفاصيلها والأماكن المتاحة، وبعدين استخدم الانضمام من شاشة التفاصيل. تقدر تحدد عدد الأماكن. الخطوة دي محتاجة حساب، لأن الضيف يقدر يتصفح من غير ما ينشئ أو يدير مباريات."),
        ("matches", "إزاي أعمل ماتش جديد؟", "سجّل دخولك بـ Google، وافتح تبويب «إنشاء». هتدخل عنوان المباراة والرياضة واسم الملعب والعنوان والمحافظة والمدينة والقرية ورقم التواصل والتاريخ والوقت وعدد اللاعبين والمستوى المطلوب والسعر لكل لاعب، وبعدين تضغط «نشر المباراة». الوصف اختياري. لو داخل كضيف، التطبيق هيطلب منك تسجيل الدخول قبل النشر."),
        ("start", "هل أقدر أستخدم التطبيق من غير حساب؟", "أيوه. من شاشة الدخول تقدر تختار «الدخول كضيف» وتتصفح المباريات. إنشاء المباراة وحذف الحساب وتعديل الملف الشخصي محتاجين تسجيل الدخول."),
        ("start", "إزاي أسجّل الدخول؟", "من شاشة تسجيل الدخول اضغط «تسجيل الدخول بـ Google». التطبيق بيستخدم حساب Google، ومفيش تسجيل دخول ظاهر بحساب تاني في الشاشة دي."),
        ("account", "إزاي أعدل بيانات البروفايل؟", "افتح «الملف الشخصي» وبعدين «تعديل الملف الشخصي». تقدر تحدّث الاسم والصورة من الكاميرا أو المعرض والنبذة والعمر والرياضات المفضلة والمركز المفضل والمحافظة والمدينة والقرية. ربط رقم الموبايل متاح من الملف الشخصي لو اخترت تضيفه."),
        ("notifications", "هل التطبيق بيبعت إشعارات؟", "أيوه. التطبيق بيطلب إذن الإشعارات وبيستخدم Firebase Cloud Messaging لتحديثات المباريات والتذكيرات وتأكيد الحضور، حسب إذن جهازك. من الإعدادات تقدر تغيّر الوضع الداكن واللغة، وإيقاف الإشعارات نفسه بيتم من إعدادات الجهاز."),
        ("safety", "إزاي أبلغ عن مشكلة؟", "من «الملف الشخصي» ثم «مركز المساعدة» تقدر تراسل الدعم أو تفتح واتساب أو تبعت بلاغ من التطبيق. كمان تقدر تستخدم صفحة التواصل هنا. وضّح نوع المشكلة والخطوات ونوع جهازك، وإصدار التطبيق ظاهر أسفل شاشة الإعدادات."),
        ("account", "إزاي أحذف حسابي؟", "لو داخل بحساب، افتح «الملف الشخصي» ثم «الإعدادات»، ومن قسم الحساب اضغط «حذف الحساب» وأكّد من النافذة. تقدر كمان تتبع التعليمات في صفحة حذف الحساب هنا لو محتاج تطلب المساعدة بالبريد."),
    ],
    "en": [
        ("start", "What is Yalla Match?", "Yalla Match is a sports application that helps you discover games, join available matches, and organize your own matches with other players. The sports you see depend on the list returned by the service."),
        ("matches", "How can I find a match near me?", "From Home, browse matches and filter them by sport and by governorate, city, or village, then open a match for its details. The app does not ask for device location permission. If a distance is shown, it comes from the match information returned by the service."),
        ("matches", "How do I join a match?", "Select a suitable match, review its details and available spots, then use the join option on the match details screen. You can choose how many spots to book. Joining is an account action. Guest mode is for browsing."),
        ("matches", "How do I create a match?", "Sign in with Google and open the Create tab. Enter the match title, sport, stadium, address, governorate, city, village, contact phone, date, time, player counts, required skill level, and price per player, then tap Publish Match. The description is optional. If you are browsing as a guest, the app asks you to sign in before publishing."),
        ("start", "Can I use Yalla Match without an account?", "Yes. On the sign-in screen, choose Join as Guest to browse matches. Creating a match, editing a profile, and deleting an account require signing in."),
        ("start", "How can I sign in?", "On the sign-in screen, tap Google Sign In. The screen uses a Google account. It does not show another sign-in method."),
        ("account", "How can I update my profile?", "Open Profile, then Edit Profile. You can update your name, photo from the camera or gallery, bio, age, favorite sports, preferred position, and governorate, city, or village. You can also link a mobile number from your profile if you choose to add one."),
        ("notifications", "Does Yalla Match send notifications?", "Yes. The app asks for notification permission and uses Firebase Cloud Messaging for match updates, reminders, and attendance confirmation, depending on your device permission. Settings lets you change dark mode and language. Notification permission itself is managed in your device settings."),
        ("safety", "How can I report an issue?", "Open Profile, then Help Center, to email support, chat on WhatsApp, or send a report inside the app. You can also use the Contact page on this site. Describe the issue, the steps that led to it, and your device. The app version is shown at the bottom of Settings."),
        ("account", "How can I delete my account?", "When you are signed in, open Profile, then Settings, and under Account tap Delete Account and confirm the dialog. You can also follow the Delete Account page on this site if you need to ask for help by email."),
    ],
}

FILTERS = {
    "ar": [("all", "الكل"), ("start", "البداية"), ("matches", "المباريات"), ("account", "الحساب والملف"), ("notifications", "الإشعارات"), ("safety", "الأمان والدعم")],
    "en": [("all", "All"), ("start", "Getting Started"), ("matches", "Matches"), ("account", "Account & Profile"), ("notifications", "Notifications"), ("safety", "Safety & Support")],
}


def render_faq(lang, path):
    title = "الأسئلة الشائعة" if lang == "ar" else "Frequently Asked Questions"
    lead = (
        "إجابات حسب طريقة عمل يلا ماتش في التطبيق الحالي."
        if lang == "ar"
        else "Answers based on how Yalla Match works in the current app."
    )
    chips = []
    for key, label in FILTERS[lang]:
        pressed = "true" if key == "all" else "false"
        chips.append(
            f'<button class="filter-chip" type="button" data-filter="{key}" aria-pressed="{pressed}">{esc(label)}</button>'
        )
    items = []
    entities = []
    for index, (category, question, answer) in enumerate(FAQ[lang], start=1):
        panel_id = f"faq-panel-{index}"
        button_id = f"faq-button-{index}"
        items.append(
            f'''<article class="faq-item" data-category="{category}">
              <h3><button id="{button_id}" type="button" aria-expanded="false" aria-controls="{panel_id}"><span>{esc(question)}</span><svg class="chevron" viewBox="0 0 24 24" aria-hidden="true"><path d="M6 9l6 6 6-6" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg></button></h3>
              <div class="faq-panel" id="{panel_id}" role="region" aria-labelledby="{button_id}"><p>{esc(answer)}</p></div>
            </article>'''
        )
        entities.append(
            '{"@type":"Question","name":'
            + json_string(question)
            + ',"acceptedAnswer":{"@type":"Answer","text":'
            + json_string(answer)
            + "}}"
        )
    return f"""
    <section class="section page-hero">
      <h1>{esc(title)}</h1>
      <p class="lead">{esc(lead)}</p>
      <div class="filters" role="group" aria-label="{esc(title)}">{''.join(chips)}</div>
      <div class="faq-list">{''.join(items)}</div>
    </section>
    <script type="application/ld+json">
    {{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{','.join(entities)}]}}
    </script>
    """


def json_string(value):
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ") + '"'


def render_contact(lang, path):
    if lang == "ar":
        title = "تواصل مع فريق يلا ماتش"
        lead = "عندك سؤال، اقتراح، أو مشكلة في التطبيق؟ فريق يلا ماتش جاهز يساعدك. اختار طريقة التواصل المناسبة ليك."
        email_title = "البريد الإلكتروني"
        email_button = "راسلنا عبر البريد الإلكتروني"
        whats_title = "واتساب"
        whats_button = "تواصل عبر واتساب"
        facebook_note = "صفحة يلا ماتش على فيسبوك. تابع التحديثات وتواصل معانا من هناك."
        facebook_button = "افتح صفحة فيسبوك"
        linkedin_note = "حساب لينكدإن لأكرم موسى، مطوّر يلا ماتش."
        linkedin_button = "افتح لينكدإن"
        report_title = "لما تبلغ عن مشكلة"
        report = "علشان نقدر نساعدك بشكل أسرع، ياريت توضح نوع المشكلة، والخطوات اللي حصلت قبل ظهورها، ونوع جهازك، وإصدار التطبيق لو متاح."
        form_title = "جهّز رسالة للدعم"
        form_note = "النموذج بيفتح مسودة في تطبيق البريد عندك. الموقع مش بيخزّن الرسالة ومش بينشئ تذكرة دعم."
        name = "الاسم (اختياري)"
        email = "البريد الإلكتروني"
        category = "نوع المشكلة"
        subject = "الموضوع"
        message = "الرسالة"
        send = "فتح مسودة البريد"
        options = [("", "اختار النوع"), ("bug", "خلل"), ("feature", "طلب ميزة"), ("account", "حساب"), ("match", "مباراة"), ("other", "أخرى")]
        intro = "رسالة من نموذج دعم يلا ماتش:"
        footer = "هذه مسودة فقط. لن تُرسل حتى يرسلها صاحبها من بريده."
        status = "اتفتحت مسودة في تطبيق البريد. الرسالة لسه ما اتبعتش، والموقع ما خزّنهاش."
        err_email = "اكتب بريد إلكتروني صحيح."
        err_category = "اختار نوع المشكلة."
        err_subject = "اكتب موضوع الرسالة."
        err_message = "اكتب تفاصيل المشكلة في 10 أحرف على الأقل."
        prefix = "دعم يلا ماتش"
    else:
        title = "Contact Yalla Match Support"
        lead = "Have a question, suggestion, or issue with the app? We're here to help. Choose your preferred way to contact us."
        email_title = "Email"
        email_button = "Send Us an Email"
        whats_title = "WhatsApp"
        whats_button = "Chat on WhatsApp"
        facebook_note = "The Yalla Match Facebook page. Follow updates and reach us there."
        facebook_button = "Open Facebook page"
        linkedin_note = "Akram Mousa’s LinkedIn, the developer behind Yalla Match."
        linkedin_button = "Open LinkedIn"
        report_title = "When you report a problem"
        report = "To help us assist you faster, please include the type of issue, the steps that led to it, your device model, and the app version if available."
        form_title = "Prepare a support email"
        form_note = "This form opens a draft in your email app. The website does not store the message and does not create a support ticket."
        name = "Name (optional)"
        email = "Email"
        category = "Issue category"
        subject = "Subject"
        message = "Message"
        send = "Open email draft"
        options = [("", "Choose a category"), ("bug", "Bug"), ("feature", "Feature request"), ("account", "Account"), ("match", "Match"), ("other", "Other")]
        intro = "Message from the Yalla Match support form:"
        footer = "This is only a draft. It is not sent until you send it from your email app."
        status = "A draft was handed to your email app. It has not been sent, and this website did not store it."
        err_email = "Enter a valid email address."
        err_category = "Choose an issue category."
        err_subject = "Enter a subject."
        err_message = "Describe the issue in at least 10 characters."
        prefix = "Yalla Match Support"
    option_html = "".join(f'<option value="{esc(value)}">{esc(label)}</option>' for value, label in options)
    return f"""
    <section class="section page-hero">
      <h1>{esc(title)}</h1>
      <p class="lead">{esc(lead)}</p>
    </section>
    <section class="section contact-grid" aria-label="{esc(title)}">
      <article class="contact-card">{icon('mail')}<h2>{esc(email_title)}</h2><p class="ltr">{EMAIL}</p><a class="button button-navy" href="mailto:{EMAIL}">{esc(email_button)}</a></article>
      <article class="contact-card">{icon('chat')}<h2>{esc(whats_title)}</h2><p class="ltr">{esc(WHATSAPP_DISPLAY)}</p><a class="button button-navy" href="{WHATSAPP_URL}" target="_blank" rel="noopener noreferrer">{esc(whats_button)}</a></article>
      <article class="contact-card"><h2>Facebook</h2><p class="social-note">{esc(facebook_note)}</p><a class="button button-ghost" href="{FACEBOOK_URL}" target="_blank" rel="noopener noreferrer">{esc(facebook_button)}</a></article>
      <article class="contact-card"><h2>LinkedIn</h2><p class="social-note">{esc(linkedin_note)}</p><a class="button button-ghost" href="{LINKEDIN_URL}" target="_blank" rel="noopener noreferrer">{esc(linkedin_button)}</a></article>
    </section>
    <section class="section panel">
      <h2>{esc(report_title)}</h2>
      <p>{esc(report)}</p>
      <h3>{esc(form_title)}</h3>
      <p>{esc(form_note)}</p>
      <form id="support-form" class="form-grid" novalidate
        data-support-email="{EMAIL}"
        data-subject-prefix="{esc(prefix)}"
        data-intro="{esc(intro)}"
        data-footer="{esc(footer)}"
        data-status-ready="{esc(status)}"
        data-label-name="{esc(name)}"
        data-label-email="{esc(email)}"
        data-label-category="{esc(category)}"
        data-label-subject="{esc(subject)}"
        data-label-message="{esc(message)}"
        data-error-email="{esc(err_email)}"
        data-error-category="{esc(err_category)}"
        data-error-subject="{esc(err_subject)}"
        data-error-message="{esc(err_message)}">
        <p id="form-error" class="form-error" hidden></p>
        <p id="form-status" class="form-status" role="status" hidden></p>
        <label>{esc(name)}<input name="name" type="text" autocomplete="name"></label>
        <label>{esc(email)}<input name="email" type="email" autocomplete="email" required class="ltr"></label>
        <label>{esc(category)}<select name="category" required>{option_html}</select></label>
        <label>{esc(subject)}<input name="subject" type="text" required></label>
        <label>{esc(message)}<textarea name="message" required></textarea></label>
        <button class="button button-navy" type="submit">{esc(send)}</button>
      </form>
    </section>
    """


def prose(blocks):
    html = []
    toc = []
    for block in blocks:
        kind = block[0]
        if kind == "h2":
            toc.append(f'<li><a href="#{esc(block[1])}">{esc(block[2])}</a></li>')
            html.append(f'<h2 id="{esc(block[1])}">{esc(block[2])}</h2>')
        elif kind == "p":
            html.append(f"<p>{esc(block[1])}</p>")
        elif kind == "ul":
            html.append("<ul>" + "".join(f"<li>{esc(item)}</li>" for item in block[1]) + "</ul>")
        elif kind == "ol":
            html.append('<ol class="steps-list">' + "".join(f"<li>{esc(item)}</li>" for item in block[1]) + "</ol>")
        elif kind == "note":
            html.append(f"<p><strong>{esc(block[1])}</strong> {esc(block[2])}</p>")
    return f'<ul class="toc">{"".join(toc)}</ul><div class="prose">{"".join(html)}</div>'


def render_privacy(lang, path):
    if lang == "ar":
        title = "سياسة الخصوصية"
        lead = "هذه الصفحة تتبع مسودة سياسة الخصوصية الموجودة في المشروع بتاريخ 12 أغسطس 2026، بعد مطابقتها مع تطبيق يلا ماتش الإصدار 1.0.2. المسودة نفسها تطلب تأكيد المالك قبل اعتماد رابط عام."
        banner_title = "تحتاج مراجعة المالك قبل النشر النهائي"
        banner = "تاريخ آخر تحديث أدناه مأخوذ من مسودة المشروع، والمسودة ما زالت تطلب التأكيد. العبارات التي تبدأ بـ «يحتاج تأكيد» ليست مثبتة في كود الخادم."
        blocks = [
            ("p", "آخر تحديث في مسودة المشروع: 12 أغسطس 2026. الجهة المذكورة في تلك المسودة كمسؤول عن البيانات: أكرم موسى. بريد الدعم: support.yallamatch@gmail.com. هاتف الدعم: ‎+20 101 926 0479."),
            ("h2", "intro", "مقدمة"),
            ("p", "يلا ماتش تطبيق يساعد اللاعبين على اكتشاف المباريات المحلية والانضمام إليها أو إنشائها. باستخدام التطبيق فأنت تستخدم الممارسات الموضحة هنا. إذا لم توافق، لا تستخدم التطبيق."),
            ("h2", "collect", "المعلومات التي يجمعها التطبيق"),
            ("ul", [
                "عند تسجيل الدخول بـ Google: رمز تعريف Google، رمز إشعارات Firebase، ونوع الجهاز (IOS أو ANDROID) تُرسل إلى خدمة يلا ماتش.",
                "بيانات الحساب القادمة من الخدمة قد تشمل الاسم والبريد ومعرّف Google والصورة ورقم الهاتف إن أُضيف والعمر والنبذة والرياضات والمركز والمحافظة والمدينة والقرية ودرجة الثقة وإحصاءات المباريات وحالة الحساب.",
                "عند إنشاء مباراة: العنوان والرياضة واسم الملعب والوصف إن وُجد وعدد اللاعبين والمستوى وعدد الأماكن والسعر لكل لاعب والمحافظة والمدينة والقرية والعنوان ورقم التواصل وموعد المباراة.",
                "بلاغات المشاكل والاقتراحات وبلاغات المباريات أو المستخدمين التي يرسلها الشخص من داخل التطبيق.",
                "تفضيلات محلية مثل اللغة والوضع الداكن ووضع الضيف، ومعرّف جهاز يُنشأ محليًا لاستمرار جلسة الضيف، ونسخ مخزنة مؤقتًا لبعض المباريات والملف الشخصي.",
                "عند إرسال ملاحظة أو بلاغ قد يُرفق إصدار التطبيق ومعلومات الجهاز الظاهرة في نموذج الدعم.",
            ]),
            ("h2", "use", "كيف تُستخدم المعلومات"),
            ("p", "الاستخدام الظاهر هو إنشاء الجلسة، عرض الملف والمباريات، التنسيق بين اللاعبين، الإشعارات التي يسمح بها الجهاز، والدعم ومراجعة البلاغات. مكتبات التطبيق لا تتضمن أداة إعلانات. مسودة السياسة تقول إن المعلومات الشخصية لا تُستخدم لعرض إعلانات طرف ثالث، وإن البيانات الشخصية لا تُباع."),
            ("note", "يحتاج تأكيد:", "عدم البيع بند مكتوب في المسودة، وليس عقدًا ظاهرًا في تطبيق الهاتف."),
            ("note", "يحتاج تأكيد:", "لا يوضح كود التطبيق إن كانت الخدمة تستخدم البيانات لاحقًا لأغراض أخرى."),
            ("h2", "location", "معلومات الموقع"),
            ("p", "التطبيق لا يطلب إذن موقع الجهاز في إعدادات أندرويد أو iOS التي رُوجعت. المكان في يلا ماتش هو المحافظة والمدينة والقرية التي يختارها الشخص، مع اسم الملعب والعنوان الذي يكتبه منظم المباراة. الشاشة الرئيسية قد تعرض مسافة إذا أرسلتها الخدمة مع بيانات المباراة."),
            ("h2", "auth", "تسجيل الدخول والحساب"),
            ("p", "تسجيل الدخول الظاهر هو Google Sign-In مع Firebase Authentication، ثم تبادل الرمز مع خدمة يلا ماتش. رمزا الوصول والتحديث يُحفظان في التخزين الآمن للجهاز. يمكن استخدام التطبيق كضيف من دون حساب، وبعض الإجراءات تطلب تسجيل الدخول."),
            ("h2", "notifications", "الإشعارات"),
            ("p", "التطبيق يطلب إذن الإشعارات ويحصل على رمز Firebase Cloud Messaging عند تسجيل الدخول. الإشعارات الظاهرة في التطبيق تشمل نشاط المباريات والتذكيرات وتأكيد الحضور. لا يوجد مفتاح مستقل للإشعارات داخل شاشة الإعدادات؛ التحكم في الإذن يتم من نظام الجهاز."),
            ("h2", "photos", "الصور وبيانات الملف"),
            ("p", "يمكن التقاط صورة شخصية بالكاميرا أو اختيارها من المعرض ثم رفعها إلى خدمة يلا ماتش. نص إذن iOS يقول إن الكاميرا ومعرض الصور مخصصان لصورة الملف الشخصي."),
            ("h2", "third", "خدمات الطرف الثالث"),
            ("ul", [
                "Google Sign-In وFirebase Authentication لتسجيل الدخول.",
                "Firebase Cloud Messaging والإشعارات المحلية على الجهاز.",
                "خدمة يلا ماتش على العنوان المستخدم في التطبيق: https://yalla-match.menuflowx.com/",
            ]),
            ("note", "يحتاج تأكيد:", "تعاقدات الاستضافة والنسخ الاحتياطي وأي معالجات أخرى غير ظاهرة في تطبيق الهاتف."),
            ("h2", "sharing", "مشاركة البيانات"),
            ("p", "بيانات الحساب والمباريات تُرسل إلى خدمة يلا ماتش. بيانات تسجيل الدخول والإشعارات تمر عبر Google وFirebase. تفاصيل المباراة، ومنها رقم تواصل المنظم والعنوان، تظهر لمن يفتح المباراة داخل التطبيق. يمكن عرض ملف لاعب آخر من داخل التطبيق. هذه الصفحة لا تقول إن البيانات لا تُشارك."),
            ("h2", "security", "التخزين والأمان"),
            ("p", "رموز الجلسة تُحفظ في التخزين الآمن للجهاز، وعنوان الخدمة المستخدم في الإصدار الحالي يبدأ بـ HTTPS. إعداد أندرويد يسمح باتصالات غير المشفرة، وإعداد iOS يسمح بالتحميل غير المقيد. لذلك هذه الصفحة لا تدّعي أن كل اتصال مشفّر أو أن كل البيانات مشفّرة في التخزين."),
            ("note", "يحتاج تأكيد:", "ضوابط الوصول على الخادم، والتشفير أثناء التخزين، وسياسة النسخ الاحتياطي."),
            ("h2", "retention", "الاحتفاظ بالبيانات"),
            ("p", "مسودة السياسة تقول إن البيانات تبقى ما دام الحساب نشطًا وللغرض اللازم لتشغيل التطبيق، وإن حذف الحساب من التطبيق يؤدي إلى حذف بيانات الحساب من الأنظمة النشطة أو إخفاء هويتها، مع ما يلزم الاحتفاظ به لأسباب قانونية أو أمنية أو لمنع الاحتيال. وتقول إن نسخًا متبقية قد تبقى مؤقتًا في النسخ الاحتياطية لفترة محدودة. البيانات المحلية على الجهاز يمكن أن تزول عند تسجيل الخروج أو مسح بيانات التطبيق أو حذفه."),
            ("note", "يحتاج تأكيد:", "كود التطبيق لا يحدد عدد الأيام، ولا يثبت ماذا يحذفه الخادم فعلًا. عبارة «فترة محدودة» ليست مدة مؤكدة."),
            ("h2", "rights", "حقوق المستخدم"),
            ("p", "يمكن تعديل جزء من بيانات الملف من شاشة تعديل الملف الشخصي، ويمكن لصاحب الحساب المسجّل طلب الحذف من الإعدادات. لا توجد في التطبيق أداة لتنزيل نسخة كاملة من البيانات."),
            ("h2", "deletion", "حذف الحساب والبيانات"),
            ("p", "شرح الخطوات موجود في صفحة حذف الحساب. رسالة التأكيد داخل التطبيق تقول إن الإجراء لا يمكن التراجع عنه، وإن الملف الشخصي والمباريات والبيانات ستُحذف نهائيًا. ما يحذفه الخادم فعليًا يحتاج تأكيد المالك."),
            ("h2", "children", "خصوصية الأطفال"),
            ("p", "مسودة السياسة تقول إن يلا ماتش غير موجّه لمن هم دون 13 عامًا، أو دون سن الموافقة الرقمية في بلد المستخدم إذا كان أعلى، وإن التطبيق لا يجمع عن علم بيانات من دون هذا السن. يمكن مراسلة الدعم لطلب حذف بيانات طفل."),
            ("note", "يحتاج تأكيد:", "التطبيق لا يضع حاجز عمر عند إنشاء الحساب. حقل العمر في الملف اختياري، وحد 12 إلى 55 داخل بيانات المباراة ليس فحصًا لعمر صاحب الحساب."),
            ("h2", "changes", "التغييرات على هذه السياسة"),
            ("p", "مسودة المشروع بتاريخ 12 أغسطس 2026 تقول إن السياسة قد تُحدَّث ويُراجع تاريخ آخر تحديث. داخل التطبيق تُعرض أقسام السياسة مما ترجعه خدمة السياسات، وقد تختلف عن هذه الصفحة إلى أن يعتمد المالك نصًا واحدًا."),
            ("h2", "contact", "التواصل"),
            ("p", "لأسئلة الخصوصية راسل support.yallamatch@gmail.com أو استخدم واتساب على ‎+20 101 926 0479. المسؤول المذكور في مسودة السياسة: أكرم موسى."),
        ]
    else:
        title = "Privacy Policy"
        lead = "This page follows the project draft in privacy_policy.md, dated 12 August 2026, after checking it against Yalla Match version 1.0.2. That draft still asks the owner to confirm it before a public URL is treated as final."
        banner_title = "Owner review required before final publication"
        banner = "The date below comes from the project draft, and the draft still asks for confirmation. Sentences that start with “Needs confirmation” are not proven in the server code."
        blocks = [
            ("p", "Draft last updated: 12 August 2026. The draft names Akram Mousa as the data controller. Support email: support.yallamatch@gmail.com. Support phone: +20 101 926 0479."),
            ("h2", "intro", "Introduction"),
            ("p", "Yalla Match helps players discover, join, and create local sports matches. If you use the app, these are the practices described for that use. If you do not agree, do not use the app."),
            ("h2", "collect", "Information the app collects"),
            ("ul", [
                "When you sign in with Google, the app sends a Google ID token, a Firebase notification token, and the platform (IOS or ANDROID) to the Yalla Match service.",
                "Account data returned by the service can include name, email, Google identifier, photo, phone number if you add one, age, bio, sports, position, governorate, city, village, trust score, match statistics, and account status.",
                "When you create a match: title, sport, stadium name, optional description, player counts, skill level, spots, price per player, governorate, city, village, address, contact phone, and match date and time.",
                "Issue reports, suggestions, and reports about a match or another user that you submit in the app.",
                "Local preferences such as language, dark mode, and guest mode, a device identifier created on the phone for guest session continuity, and cached copies of some matches and profile data.",
                "Feedback or a report can include the app version and the device details shown in the support form.",
            ]),
            ("h2", "use", "How information is used"),
            ("p", "The visible uses are creating a session, showing the profile and matches, coordinating players, sending notifications the device allows, and handling support and reports. The app dependencies do not include an advertising SDK. The project draft says personal information is not used to show third-party ads and is not sold."),
            ("note", "Needs confirmation:", "The “not sold” statement is written in the draft. It is not a contract visible inside the mobile app."),
            ("note", "Needs confirmation:", "The app code does not show whether the service later uses data for any other purpose."),
            ("h2", "location", "Location information"),
            ("p", "The reviewed Android and iOS permission lists do not request device location. Location in Yalla Match is the governorate, city, and village a person selects, plus the stadium name and address typed by the match organizer. Home can show a distance when the service includes one with the match."),
            ("h2", "auth", "Authentication and account information"),
            ("p", "The visible sign-in method is Google Sign-In with Firebase Authentication, followed by an exchange with the Yalla Match service. Access and refresh tokens are stored in the device secure storage. You can browse as a guest without an account, and some actions require signing in."),
            ("h2", "notifications", "Notifications"),
            ("p", "The app requests notification permission and reads a Firebase Cloud Messaging token at sign-in. The notification types visible in the app include match activity, reminders, and attendance confirmation. Settings does not include a separate notification switch. Permission is controlled by the device."),
            ("h2", "photos", "Photos and profile information"),
            ("p", "You can take a profile photo with the camera or choose one from the photo library and upload it to the Yalla Match service. The iOS permission text says camera and photo library access are for the profile photo."),
            ("h2", "third", "Third-party services"),
            ("ul", [
                "Google Sign-In and Firebase Authentication for sign-in.",
                "Firebase Cloud Messaging and on-device local notifications.",
                "The Yalla Match service at the address used by the app: https://yalla-match.menuflowx.com/",
            ]),
            ("note", "Needs confirmation:", "Hosting contracts, backups, and any processors that are not visible in the mobile app."),
            ("h2", "sharing", "Data sharing"),
            ("p", "Account and match data are sent to the Yalla Match service. Sign-in and notification data pass through Google and Firebase. Match details, including the organizer phone number and address, are shown to people who open that match in the app. Another player's profile can be opened in the app. This page does not claim that data is never shared."),
            ("h2", "security", "Data storage and security"),
            ("p", "Session tokens are stored in device secure storage, and the service address in the current version uses HTTPS. The Android configuration allows cleartext traffic, and the iOS configuration allows arbitrary loads. This page does not claim that every connection is encrypted or that all stored data is encrypted."),
            ("note", "Needs confirmation:", "Server access controls, encryption at rest, and the backup policy."),
            ("h2", "retention", "Data retention"),
            ("p", "The project draft says data is kept while the account is active and as needed to run the app. It says an in-app deletion deletes or anonymizes account data on active systems, except data that must be kept for legal, security, dispute, or fraud-prevention reasons, and that leftover copies may remain in backups for a limited period. Data stored only on the phone can be removed by signing out, clearing app data, or uninstalling."),
            ("note", "Needs confirmation:", "The app code does not set a number of days, and it does not prove what the server deletes. “A limited period” is not a confirmed duration."),
            ("h2", "rights", "User rights"),
            ("p", "You can edit part of your profile in Edit Profile, and a signed-in user can request deletion from Settings. The app does not include a tool to download a full copy of personal data."),
            ("h2", "deletion", "Account and data deletion"),
            ("p", "The steps are explained on the Delete Account page. The in-app confirmation says the action cannot be undone and that the profile, matches, and data will be permanently deleted. What the server actually deletes still needs owner confirmation."),
            ("h2", "children", "Children's privacy"),
            ("p", "The project draft says Yalla Match is not directed to children under 13, or under a higher digital-consent age where that applies, and that the app does not knowingly collect personal information from children under that age. A parent can email support and ask for that information to be deleted."),
            ("note", "Needs confirmation:", "The app does not block account creation with an age gate. Profile age is optional, and the 12 to 55 range sent with a match is not a check of the account holder's age."),
            ("h2", "changes", "Changes to this policy"),
            ("p", "The project draft dated 12 August 2026 says the policy may be updated and the last-updated date revised. Inside the app, policy sections come from the policies service and may differ from this page until the owner publishes one text."),
            ("h2", "contact", "Contact us"),
            ("p", "For privacy questions, email support.yallamatch@gmail.com or use WhatsApp on +20 101 926 0479. The draft names Akram Mousa as the person responsible for the data."),
        ]
    return f"""
    <section class="section page-hero prose">
      <h1>{esc(title)}</h1>
      <p class="lead">{esc(lead)}</p>
      <div class="review-banner"><strong>{esc(banner_title)}</strong><p>{esc(banner)}</p></div>
      {prose(blocks)}
    </section>
    """


def render_terms(lang, path):
    if lang == "ar":
        title = "الشروط والأحكام"
        lead = "هذه الشروط تصف دور يلا ماتش كما يظهر في التطبيق: مكان لتنسيق المباريات بين اللاعبين. البنود غير الظاهرة في التطبيق معلّمة للمراجعة، ولا تُعامل كنص نهائي قبل اعتماد المالك."
        banner_title = "تحتاج مراجعة قانونية قبل النشر النهائي"
        banner = "التطبيق لا يحدد اشتراكًا مدفوعًا أو تأمينًا أو قانونًا واجب التطبيق أو سقفًا ماليًا للمسؤولية. لا تفترض هذه الصفحة أيًا من ذلك."
        blocks = [
            ("h2", "accept", "قبول الشروط"),
            ("p", "باستخدام يلا ماتش فأنت تستخدم أداة لتنسيق المباريات الرياضية بين الأشخاص. إذا لم توافق على هذه الشروط بعد اعتمادها، فيمكنك التوقف عن استخدام التطبيق وطلب حذف الحساب إن كان لديك حساب."),
            ("h2", "about", "وصف يلا ماتش"),
            ("p", "يلا ماتش يساعد على تصفح المباريات حسب الرياضة والمنطقة، وإنشاء مباراة، والانضمام إلى مباراة، وإدارة المباريات التي أنشأتها أو انضممت إليها. يلا ماتش ليس، حسب ما يظهر في التطبيق، مالكًا أو مشغّلًا للملاعب."),
            ("h2", "eligibility", "الأهلية والحسابات"),
            ("p", "يمكن تصفح المباريات كضيف. إنشاء المباراة وتعديل الملف وحذف الحساب تحتاج تسجيل الدخول بـ Google. لا يظهر في التطبيق حد عمر مؤكد لإنشاء الحساب."),
            ("note", "يحتاج تأكيد:", "من يُسمح له بإنشاء حساب، وهل يوجد حد أدنى للسن."),
            ("h2", "responsibility", "مسؤولية الحساب"),
            ("p", "صاحب الحساب مسؤول عن النشاط الذي يتم أثناء تسجيل دخوله، وعن صحة الاسم وبيانات المباراة ورقم التواصل الذي يكتبه. لا تشارك كلمة مرور Google أو رموز التحقق مع الدعم."),
            ("h2", "matches", "إنشاء المباريات والانضمام إليها"),
            ("p", "المنظم يدخل تفاصيل المباراة، ومنها الموعد والملعب والعنوان والسعر لكل لاعب ورقم التواصل. السعر يُسجل في التطبيق بالجنيه. لا توجد في التطبيق أداة دفع إلكتروني. نص المساعدة داخل التطبيق يقول إن بعض المباريات لها رسم لكل لاعب يظهر في التفاصيل، وإن التحصيل يتم عبر المنظم ما لم يُذكر غير ذلك."),
            ("note", "يحتاج تأكيد:", "أي سياسة استرداد أو نزاع مالي. التطبيق لا يحتوي سياسة استرداد."),
            ("h2", "organizer", "مسؤولية المنظم"),
            ("p", "المنظم هو من ينشر تفاصيل المباراة ورقم التواصل. التطبيق يتيح للمنظم إزالة لاعب من مباراته أو حظره عن تلك المباراة. التطبيق لا يتحقق من هوية المنظم ولا يضمن أن الملعب متاح."),
            ("h2", "player", "مسؤولية اللاعب"),
            ("p", "اللاعب يراجع تفاصيل المباراة قبل الانضمام، ويختار عدد الأماكن. التطبيق يتضمن تأكيد حضور ودرجة ثقة. لا تحدد هذه الصفحة جزاءً محددًا عند عدم الحضور لأن قواعد الدرجة على الخادم غير ظاهرة هنا."),
            ("h2", "conduct", "سلوك المستخدم"),
            ("p", "أسباب البلاغ الظاهرة في التطبيق تشمل الحجز الوهمي والمضايقة وعدم الحضور والسلوك غير اللائق. لا تستخدم التطبيق للإساءة إلى اللاعبين أو لنشر معلومات مضللة عن مباراة."),
            ("h2", "safety", "أمان المجتمع"),
            ("p", "قابل اللاعبين في أماكن عامة واتخذ احتياطك الشخصي. يلا ماتش أداة تنسيق ولا يرافق اللاعبين في الملعب."),
            ("h2", "content", "المحتوى الذي يضيفه المستخدم"),
            ("p", "النصوص والصور وتفاصيل المباريات التي تضيفها تُرسل إلى خدمة يلا ماتش وقد يراها مستخدمون آخرون حسب شاشات التطبيق. أنت مسؤول عن امتلاك الحق في الصورة أو النص الذي ترفعه."),
            ("h2", "reports", "البلاغات والإشراف"),
            ("p", "يمكن الإبلاغ عن مباراة أو مستخدم أو إرسال مشكلة أو اقتراح من مركز المساعدة. التطبيق يقول إن الفريق سيراجع البلاغ. معايير الإزالة أو الإيقاف غير منشورة داخل التطبيق."),
            ("note", "يحتاج تأكيد:", "مدة المراجعة، ومتى يُغلق الحساب أو تُحذف مباراة."),
            ("h2", "venues", "الملاعب والمنظمون من الغير"),
            ("p", "الملعب والموعد والسعر ورقم التواصل يأتيان من المنظم. يلا ماتش لا يملك الملعب ولا يضمن حالته أو توفره أو أن المباراة ستقام."),
            ("h2", "availability", "توفر الخدمة"),
            ("p", "قد يتعذر تحميل المباريات أو نشرها عند انقطاع الشبكة أو توقف الخدمة. التطبيق لا يعد بتوفر دائم."),
            ("h2", "suspension", "إيقاف الحساب أو إنهاؤه"),
            ("p", "بيانات الحساب تتضمن حالة، لكن التطبيق لا ينشر قواعد الإيقاف. يمكنك أنت حذف حسابك من الإعدادات كما هو موضح في صفحة حذف الحساب."),
            ("note", "يحتاج تأكيد:", "الحالات التي يوقف فيها يلا ماتش حسابًا أو مباراة."),
            ("h2", "warranty", "إخلاء الضمان"),
            ("p", "التطبيق يُقدَّم كأداة تنسيق بين اللاعبين. لا يضمن التطبيق وجود مباراة مناسبة أو مهارة اللاعبين أو سلامة الملعب."),
            ("h2", "liability", "حدود المسؤولية"),
            ("p", "يلا ماتش لا يحدد في التطبيق سقفًا ماليًا للمسؤولية. إلى أن يعتمد المالك بندًا قانونيًا، لا تدّعي هذه الصفحة حدًا رقميًا أو إعفاءً يتجاوز ما يسمح به القانون."),
            ("note", "يحتاج تأكيد:", "نص حدود المسؤولية الذي يوافق عليه المالك ومستشاره القانوني."),
            ("h2", "changes", "تغيير الشروط"),
            ("p", "قد تُحدَّث هذه الصفحة عند تغيّر التطبيق أو بعد اعتماد المالك. لا يوجد تاريخ سريان مؤكد بعد."),
            ("h2", "law", "القانون الواجب التطبيق"),
            ("p", "التطبيق موجه لاستخدام المحافظات المصرية ويعرض السعر بالجنيه، لكن كود التطبيق لا يسمي قانونًا أو محكمة للفصل في النزاعات."),
            ("note", "يحتاج تأكيد:", "القانون الواجب التطبيق وجهة تسوية النزاع."),
            ("h2", "contact", "معلومات التواصل"),
            ("p", "لأي سؤال عن هذه الشروط راسل support.yallamatch@gmail.com."),
        ]
    else:
        title = "Terms & Conditions"
        lead = "These terms describe Yalla Match as the app presents it: a way for players to coordinate sports matches. Items that are not stated in the app are marked for review and are not final until the owner approves them."
        banner_title = "Legal review required before final publication"
        banner = "The app does not state a paid subscription, insurance, governing law, or a numeric liability cap. This page does not invent those terms."
        blocks = [
            ("h2", "accept", "Acceptance of terms"),
            ("p", "Yalla Match is a tool for coordinating sports matches between people. If you do not agree with these terms after they are approved, you can stop using the app and request deletion of an account you created."),
            ("h2", "about", "Description of Yalla Match"),
            ("p", "Yalla Match helps you browse matches by sport and area, create a match, join a match, and manage matches you created or joined. Nothing in the app shows that Yalla Match owns or operates sports venues."),
            ("h2", "eligibility", "Eligibility and accounts"),
            ("p", "You can browse matches as a guest. Creating a match, editing a profile, and deleting an account require Google sign-in. The app does not show a confirmed age limit for creating an account."),
            ("note", "Needs confirmation:", "Who may create an account, and whether a minimum age applies."),
            ("h2", "responsibility", "Account responsibilities"),
            ("p", "You are responsible for activity while you are signed in, and for the name, match details, and contact number you enter. Do not send your Google password or verification codes to support."),
            ("h2", "matches", "Creating and joining matches"),
            ("p", "The organizer enters the match details, including time, stadium, address, price per player, and contact phone. The price is recorded in Egyptian pounds. The app does not include an in-app payment provider. The in-app help text says some matches show a per-player fee and that collection is through the organizer unless stated otherwise."),
            ("note", "Needs confirmation:", "Any refund or payment-dispute policy. The app does not contain a refund policy."),
            ("h2", "organizer", "Organizer responsibilities"),
            ("p", "The organizer publishes the match details and contact number. The app lets an organizer remove a player from their match or block that player from that match. The app does not verify an organizer's identity and does not guarantee that a venue is available."),
            ("h2", "player", "Player responsibilities"),
            ("p", "Review the match details before joining, and choose how many spots to book. The app includes attendance confirmation and a trust score. This page does not set a specific penalty for a no-show, because the server rules for that score are not visible here."),
            ("h2", "conduct", "User conduct"),
            ("p", "The report reasons shown in the app include fake bookings, harassment, no-shows, and inappropriate behavior. Do not use the app to harm players or to publish misleading match information."),
            ("h2", "safety", "Community safety"),
            ("p", "Meet in public places and use your own judgment. Yalla Match is a coordination tool and does not accompany players at the venue."),
            ("h2", "content", "User-generated content"),
            ("p", "Text, photos, and match details you add are sent to the Yalla Match service and may be visible to other users on the screens that show them. You are responsible for having the right to upload that photo or text."),
            ("h2", "reports", "Reporting and moderation"),
            ("p", "You can report a match or user, or send a problem or suggestion from Help Center. The app says the team will review a report. Removal and suspension criteria are not published in the app."),
            ("note", "Needs confirmation:", "Review time, and when an account or match is closed."),
            ("h2", "venues", "Third-party venues and organizers"),
            ("p", "The venue, time, price, and phone number come from the organizer. Yalla Match does not own the venue and does not guarantee its condition, its availability, or that the match will take place."),
            ("h2", "availability", "Service availability"),
            ("p", "Matches may fail to load or publish when the network or the service is unavailable. The app does not promise uninterrupted service."),
            ("h2", "suspension", "Account suspension or termination"),
            ("p", "Account data includes a status, but the app does not publish suspension rules. You can delete your own account from Settings, as described on the Delete Account page."),
            ("note", "Needs confirmation:", "The cases in which Yalla Match suspends an account or a match."),
            ("h2", "warranty", "Disclaimer of warranties"),
            ("p", "The app is offered as a coordination tool between players. It does not guarantee that a suitable match exists, that players have a particular skill, or that a venue is safe."),
            ("h2", "liability", "Limitation of liability"),
            ("p", "The app does not state a numeric liability cap. Until the owner approves a legal clause, this page does not claim a dollar limit or a waiver beyond what the law allows."),
            ("note", "Needs confirmation:", "The limitation wording approved by the owner and legal counsel."),
            ("h2", "changes", "Changes to these terms"),
            ("p", "This page may be updated when the app changes or after the owner approves the text. No effective date is confirmed yet."),
            ("h2", "law", "Governing law"),
            ("p", "The app is aimed at Egyptian governorates and shows prices in Egyptian pounds, but the app code does not name a governing law or a court."),
            ("note", "Needs confirmation:", "The governing law and where a dispute would be handled."),
            ("h2", "contact", "Contact information"),
            ("p", "Questions about these terms can be sent to support.yallamatch@gmail.com."),
        ]
    return f"""
    <section class="section page-hero">
      <h1>{esc(title)}</h1>
      <p class="lead">{esc(lead)}</p>
      <div class="review-banner"><strong>{esc(banner_title)}</strong><p>{esc(banner)}</p></div>
      {prose(blocks)}
    </section>
    """


def render_delete(lang, path):
    contact = page_href(path, lang, "contact/")
    if lang == "ar":
        title = "حذف حساب يلا ماتش"
        lead = "لو حابب تحذف حسابك من يلا ماتش، تقدر تتبع الخطوات الموضحة هنا أو تتواصل مع فريق الدعم لطلب المساعدة."
        banner_title = "جزء من تفاصيل الحذف ما زال يحتاج تأكيد المالك"
        banner = "خطوات الحذف داخل التطبيق مؤكدة من الكود. مدة الاحتفاظ وأي بيانات تبقى بعد الحذف ووقت معالجة طلب البريد غير مذكورة في التطبيق، فلا تدّعي هذه الصفحة أرقامًا لها."
        in_app = "الحذف من داخل التطبيق"
        steps = [
            "افتح يلا ماتش وسجّل الدخول بـ Google. وضع الضيف لا يظهر فيه حذف الحساب لأنه لا يوجد حساب.",
            "افتح تبويب «الملف الشخصي».",
            "اضغط «الإعدادات».",
            "من قسم «الحساب» اضغط «حذف الحساب».",
            "ستظهر نافذة بعنوان «حذف الحساب؟» ونصها: «لا يمكن التراجع عن هذا الإجراء. سيتم حذف ملفك الشخصي والمباريات والبيانات نهائيًا.»",
            "اضغط «حذف الحساب» للتأكيد. التطبيق يرسل طلب حذف إلى خدمة يلا ماتش. عند النجاح يسجّل خروجك، ويلغي ربط Google الخاص بالتطبيق، وتظهر رسالة «تم حذف الحساب بنجاح».",
        ]
        verified = "ما الذي يتم التحقق منه؟"
        verified_body = "الحذف من التطبيق يتم وأنت مسجّل الدخول، أي أن الطلب مرتبط بجلسة الحساب. طلب البريد لا يحذف الحساب لحظة إرساله، ويحتاج أن يتأكد الدعم من صاحب الحساب بطريقة لا تطلب كلمة المرور أو رمز التحقق."
        deleted = "ما الذي يقول التطبيق إنه يُحذف؟"
        deleted_body = "نص النافذة يقول إن الملف الشخصي والمباريات والبيانات ستُحذف نهائيًا. رد الخدمة قد يتضمن رسالة ووقت حذف. الكود لا يعدد الجداول أو النسخ الاحتياطية أو رموز الإشعارات أو البلاغات التي يحذفها الخادم."
        retain = "ما الذي قد يُحتفظ به؟"
        retain_body = "مسودة سياسة الخصوصية بتاريخ 12 أغسطس 2026 تقول إن الحذف من التطبيق يزيل بيانات الحساب من الأنظمة النشطة أو يخفي هويتها، مع ما يجب إبقاؤه لأسباب قانونية أو أمنية أو لمنع الاحتيال، وإن نسخًا قد تبقى في النسخ الاحتياطية لفترة غير محددة برقم. كود التطبيق لا يؤكد هذا السلوك على الخادم، لذلك لا تُذكر هنا مدة بالأيام."
        email_title = "لو لم تستطع الحذف من التطبيق"
        email_body = "يمكنك إرسال طلب بالبريد. اكتب بريد حساب Google المستخدم في التطبيق، ولا ترسل كلمة مرور أو رمز تحقق."
        email_button = "طلب حذف الحساب عبر البريد"
        more = "لأي استفسار آخر استخدم صفحة التواصل."
    else:
        title = "Delete Your Yalla Match Account"
        lead = "If you would like to delete your Yalla Match account, follow the instructions below or contact our support team for assistance."
        banner_title = "Some deletion details still need owner confirmation"
        banner = "The in-app steps below are confirmed in the app code. Retention, any data that remains, and the time needed to process an email request are not stated in the app, so this page does not invent those numbers."
        in_app = "Delete the account in the app"
        steps = [
            "Open Yalla Match and sign in with Google. Guest mode does not show account deletion because there is no account.",
            "Open the Profile tab.",
            "Tap Settings.",
            "Under Account, tap Delete Account.",
            "A dialog titled “Delete Account?” says: “This action cannot be undone. Your profile, matches, and data will be permanently deleted.”",
            "Tap Delete Account to confirm. The app sends a deletion request to the Yalla Match service. On success it signs you out, revokes the Google session used by the app, and shows “Account deleted successfully”.",
        ]
        verified = "How is a request verified?"
        verified_body = "In-app deletion happens while you are signed in, so the request is tied to that account session. An email does not delete the account at the moment you send it. Support still has to confirm the account holder without asking for a password or a one-time code."
        deleted = "What does the app say is deleted?"
        deleted_body = "The dialog says the profile, matches, and data will be permanently deleted. The service response can include a message and a deletion time. The app code does not list which server records, backups, notification tokens, or reports the server removes."
        retain = "What might be retained?"
        retain_body = "The privacy draft dated 12 August 2026 says in-app deletion removes or anonymizes account data on active systems, except what must be kept for legal, security, or fraud-prevention reasons, and that copies may remain in backups for a period that is not given as a number of days. The app code does not prove that server behavior, so this page states no day count."
        email_title = "If you cannot delete it in the app"
        email_body = "You can send an email request. Include the Google account email you use in the app. Do not send a password or a verification code."
        email_button = "Request Account Deletion by Email"
        more = "For any other question, use the Contact page."
    return f"""
    <section class="section page-hero">
      <h1>{esc(title)}</h1>
      <p class="lead">{esc(lead)}</p>
      <div class="review-banner"><strong>{esc(banner_title)}</strong><p>{esc(banner)}</p></div>
    </section>
    <section class="section panel">
      <h2>{esc(in_app)}</h2>
      <ol class="steps-list">{''.join(f'<li>{esc(step)}</li>' for step in steps)}</ol>
      <h2>{esc(verified)}</h2>
      <p>{esc(verified_body)}</p>
      <h2>{esc(deleted)}</h2>
      <p>{esc(deleted_body)}</p>
      <h2>{esc(retain)}</h2>
      <p>{esc(retain_body)}</p>
      <h2>{esc(email_title)}</h2>
      <p>{esc(email_body)}</p>
      <p><a class="button button-danger" href="{esc(DELETE_MAILTO)}">{esc(email_button)}</a></p>
      <p><a href="{esc(contact)}">{esc(more)}</a></p>
    </section>
    """


META = {
    "home": {
        "ar": ("مركز دعم يلا ماتش | المساعدة والتواصل", "مركز دعم يلا ماتش لمساعدتك في استخدام التطبيق، والإجابة عن الأسئلة الشائعة، والتواصل مع الدعم الفني، ومعرفة معلومات الخصوصية والحساب."),
        "en": ("Yalla Match Support | Help Center & Contact", "Get help with Yalla Match. Find answers to common questions, contact support, review privacy information, and learn how to manage your account."),
    },
    "faq": {
        "ar": ("الأسئلة الشائعة | مركز دعم يلا ماتش", "إجابات عن التسجيل، إيجاد المباريات، إنشاء مباراة، الإشعارات، وحذف الحساب في يلا ماتش."),
        "en": ("FAQ | Yalla Match Support", "Answers about signing in, finding matches, creating a game, notifications, and deleting your Yalla Match account."),
    },
    "contact": {
        "ar": ("تواصل معنا | مركز دعم يلا ماتش", "راسل دعم يلا ماتش بالبريد أو واتساب، أو جهّز مسودة بلاغ عن مشكلة في التطبيق."),
        "en": ("Contact Us | Yalla Match Support", "Email or WhatsApp Yalla Match support, or prepare a draft report about a problem in the app."),
    },
    "privacy": {
        "ar": ("سياسة الخصوصية | يلا ماتش", "كيف يتعامل تطبيق يلا ماتش مع الحساب والمباريات والصور والإشعارات، مع توضيح ما يحتاج تأكيد المالك."),
        "en": ("Privacy Policy | Yalla Match", "How the Yalla Match app handles accounts, matches, photos, and notifications, including items that still need owner confirmation."),
    },
    "terms": {
        "ar": ("الشروط والأحكام | يلا ماتش", "شروط استخدام يلا ماتش لتنسيق المباريات بين اللاعبين، مع البنود التي تحتاج مراجعة قانونية."),
        "en": ("Terms & Conditions | Yalla Match", "Terms for using Yalla Match to coordinate matches between players, including clauses that need legal review."),
    },
    "delete": {
        "ar": ("حذف الحساب | يلا ماتش", "خطوات حذف حساب يلا ماتش من الإعدادات، وطريقة طلب الحذف بالبريد من دون إرسال كلمة المرور."),
        "en": ("Delete Account | Yalla Match", "How to delete a Yalla Match account from Settings, and how to request deletion by email without sending a password."),
    },
}

RENDERERS = {
    "home": render_home,
    "faq": render_faq,
    "contact": render_contact,
    "privacy": render_privacy,
    "terms": render_terms,
    "delete": render_delete,
}


def write_pages():
    for lang in ("ar", "en"):
        for page_id, _labels, path in PAGES:
            title, description = META[page_id][lang]
            body = RENDERERS[page_id](lang, path)
            html = layout(lang, page_id, path, title, description, body)
            destination = ROOT / lang / path / "index.html"
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(html, encoding="utf-8")
            print(destination.relative_to(ROOT))


def write_root():
    icon_src = "assets/images/app-icon.png"
    html = f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>مركز دعم يلا ماتش | المساعدة والتواصل</title>
  <meta name="description" content="مركز دعم يلا ماتش لمساعدتك في استخدام التطبيق، والإجابة عن الأسئلة الشائعة، والتواصل مع الدعم الفني، ومعرفة معلومات الخصوصية والحساب.">
  <link rel="canonical" href="ar/">
  <link rel="alternate" hreflang="ar" href="ar/">
  <link rel="alternate" hreflang="en" href="en/">
  <link rel="alternate" hreflang="x-default" href="ar/">
  <meta name="theme-color" content="#01234D">
  <link rel="icon" type="image/png" href="assets/images/favicon-32.png">
  <link rel="apple-touch-icon" href="assets/images/apple-touch-icon.png">
  <link rel="stylesheet" href="assets/css/site.css">
  <script>
    (function () {{
      var lang = "ar";
      try {{
        var saved = localStorage.getItem("yalla-match-lang");
        if (saved === "en" || saved === "ar") lang = saved;
      }} catch (error) {{}}
      location.replace(lang + "/");
    }})();
  </script>
</head>
<body>
  <main class="gate">
    <section class="gate-card">
      <img src="{icon_src}" alt="" width="84" height="84">
      <h1>يلا ماتش</h1>
      <p>مركز الدعم الرسمي. اختر اللغة إذا لم ينتقل المتصفح تلقائيًا.</p>
      <div class="gate-actions">
        <a class="button button-navy" href="ar/" data-lang-link="ar">العربية</a>
        <a class="button button-ghost" href="en/" data-lang-link="en">English</a>
      </div>
    </section>
  </main>
  <script src="assets/js/site-config.js"></script>
  <script src="assets/js/site.js"></script>
</body>
</html>
"""
    (ROOT / "index.html").write_text(html, encoding="utf-8")
    not_found = """<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>الصفحة غير موجودة | يلا ماتش</title>
  <meta name="robots" content="noindex">
  <link rel="icon" type="image/png" href="assets/images/favicon-32.png">
  <link rel="stylesheet" href="assets/css/site.css">
</head>
<body>
  <main class="gate">
    <section class="gate-card">
      <img src="assets/images/app-icon.png" alt="" width="84" height="84">
      <h1>الصفحة غير موجودة</h1>
      <p>Page not found.</p>
      <div class="gate-actions">
        <a class="button button-navy" href="ar/">العربية</a>
        <a class="button button-ghost" href="en/">English</a>
      </div>
    </section>
  </main>
</body>
</html>
"""
    (ROOT / "404.html").write_text(not_found, encoding="utf-8")
    (ROOT / ".nojekyll").write_text("", encoding="utf-8")


def write_seo():
    paths = ["", "ar/", "en/"]
    for _page_id, _labels, path in PAGES:
        if path:
            paths.append(f"ar/{path}")
            paths.append(f"en/{path}")
    urls = "\n".join(
        f"  <url><loc>{SITE_PLACEHOLDER}/{path}</loc></url>" if path else f"  <url><loc>{SITE_PLACEHOLDER}/</loc></url>"
        for path in paths
    )
    sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<!-- Replace YOUR_GITHUB_USERNAME and YOUR_REPOSITORY_NAME with the real GitHub Pages project URL before relying on this file. -->
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{urls}
</urlset>
"""
    (ROOT / "sitemap.xml").write_text(sitemap, encoding="utf-8")
    robots = f"""User-agent: *
Allow: /

Sitemap: {SITE_PLACEHOLDER}/sitemap.xml
"""
    (ROOT / "robots.txt").write_text(robots, encoding="utf-8")


def write_favicon():
    png = (ROOT / "assets/images/favicon-32.png").read_bytes()
    if not png.startswith(b"\x89PNG"):
        raise SystemExit("favicon png missing")
    header = struct.pack("<HHH", 0, 1, 1)
    entry = struct.pack("<BBBBHHII", 32, 32, 0, 0, 1, 32, len(png), 22)
    (ROOT / "favicon.ico").write_bytes(header + entry + png)
    (ROOT / "assets/images/favicon.ico").write_bytes(header + entry + png)


def main():
    write_pages()
    write_root()
    write_seo()
    write_favicon()
    print("generated")


if __name__ == "__main__":
    main()
