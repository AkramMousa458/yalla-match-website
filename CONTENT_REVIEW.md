# Content review

This file separates what was verified in the Flutter project from what the support site must not claim yet.

Reviewed app version in `pubspec.yaml`: `1.0.2+4`.

The website does not copy Firebase config, signing files, or the commented map key in `lib/core/utils/app_string.dart`.

## Verified application features

These are implemented in the current Flutter client:

- Browse matches from Home, including sport filters and governorate, city, and village filters.
- Home can show a distance when the service sends `distanceKm`. The app does not request device GPS permission.
- Create a match from the Create tab. Required fields include title, sport, stadium, detailed address, governorate, city, village when required, contact phone, date, time, total players, needed players, and price per player in EGP. Description is optional. Skill level is part of the create flow. Publishing is blocked for guests.
- Join a match from match details, including a choice of how many spots to book.
- My matches areas for upcoming, joined, created, and history views exist in the client.
- Profile fields include name, photo, bio, age, favorite sports, preferred sport and position, and governorate, city, and village. A phone number can be linked from the profile.
- Sign in with Google, through Google Sign-In and Firebase Authentication, then `POST api/auth/google` with the Google ID token, FCM token, and platform.
- Guest browsing from “Join as Guest” / «الدخول كضيف». Guests do not get profile editing or account deletion.
- Notifications through Firebase Cloud Messaging and local notifications, including match reminders and attendance confirmation actions.
- Share match UI exists (`share_plus`).
- Organizer contact phone can be opened with the phone dialer from match access details.
- In-app reports for issues, feature suggestions, matches, and users.
- Help Center contacts the same support email and WhatsApp number used on this website.
- Settings contains dark mode, language, the privacy policy screen, app version, and account deletion for signed-in users.
- Account deletion calls `DELETE api/users/me`, then signs out and revokes the Google session used by the app. The confirmation copy is the string `delete_account_message`.
- The in-app privacy screen loads policies from `GET api/policies`. It can be empty. The policy body is not stored in the repository.
- Sports shown in the client strings include football, padel, basketball, and volleyball. The live list comes from `GET api/sports`.
- Organizers can remove or block a player on their match through the bookings API.
- There is no in-app payment SDK. The in-app help text says per-player fees are collected by the organizer unless stated otherwise.
- No advertising SDK and no Firebase Analytics or Crashlytics package are listed in `pubspec.yaml`.

The supplied FAQ was adjusted where the app differs:

- Finding a match uses sport and area filters, not a device-location permission.
- Creating a match uses the Create tab and Publish Match, and it collects price, address, and a contact phone in addition to sport, venue, time, skill, and spots.
- Sign-in on the login screen is Google, not a generic account form.
- Notifications are controlled by the device permission. Settings itself toggles theme and language.
- Account deletion exists in the app. The website explains that path and keeps email as a fallback.

Not advertised because they are not a visible Yalla Match flow: phone OTP, email OTP, orders, and addresses. Those endpoint constants exist in `lib/core/utils/endpoint.dart` and are not wired to the current screens that were reviewed.

## Design tokens extracted from Flutter

Source files:

- `lib/core/utils/app_colors.dart`
- `lib/core/theme/theme_light.dart`
- `lib/core/theme/theme_dark.dart`
- `lib/core/utils/app_string.dart`
- `lib/features/home/presentation/utils/home_ui.dart`
- Card radius `24` and icon tile radius `12` from settings and help-center cards
- Pill button radius `30` from the elevated button theme
- Input radius `12` from the input decoration theme
- Launcher background `#031020` from `pubspec.yaml` `adaptive_icon_background`

| Token | Value | Source |
| --- | --- | --- |
| Primary | `#01234D` | `AppColors.primary` |
| Primary dark | `#031020` | Adaptive icon background |
| Secondary / home accent | `#7DC84D` | `AppColors.secondary` and `homeAccentLight` |
| Background | `#F1F5F9` | `AppColors.lightScaffold` |
| Surface | `#FFFFFF` | `AppColors.lightCard` |
| Text primary | `#0F172A` | `AppColors.lightTextPrimary` |
| Text secondary | `#64748B` | `AppColors.lightTextSecondary` |
| Body copy | `#334155` | `AppColors.darkInputFill`, used for long text so it stays readable on the light background |
| Border | `#E2E8F0` | `AppColors.lightBorder` |
| Input fill | `#F8FAFC` | `AppColors.lightInputFill` |
| Error | `#F04438` | `AppColors.error500` |
| Warning | `#F79009` | `AppColors.warning500` |
| Success | `#12B76A` | `AppColors.success500` |
| Card radius | `24px` | Settings and help cards |
| Button radius | `30px` | Elevated buttons |
| Input radius | `12px` | Text fields |
| Font | Tajawal 400, 500, 700, 800 | `AppString.fontFamily` and `assets/fonts` |

The public site uses the light theme. The app also has a dark theme. It was not copied onto the website because the support pages are read as documents.

Cards use a border plus a light shadow. The Flutter cards rely mainly on the border.

## Assets reused

Copied into `assets/images` and `assets/fonts`:

- `assets/icon/app_icon.png` for the hero, download mark, favicon, and social preview
- `assets/images/logo-horizontal.png` in the header, matching `CustomAppHeader` and `LoginLogo`
- `assets/images/logo-horizontal-white.png` in the footer for use on the navy background
- `assets/images/logo.png` and `logo-white.png` kept with the site for the same artwork used on the splash screen
- Tajawal font files, with `assets/fonts/OFL.txt`

The wordmarks were not redrawn. The square launcher icon is used where a square mark is needed.

No screenshots of the running app were found in the repository.

## Legal details requiring confirmation

- Governing law and dispute venue. The product uses Egyptian locations and EGP prices. The app does not name a law.
- Any liability cap or warranty wording counsel wants to publish.
- Account eligibility and minimum age.
- When Yalla Match may suspend an account or remove a match, and how fast reports are reviewed.
- Refunds or payment disputes. The app records a price and says the organizer collects it. It does not process payments.
- Whether organizers or venues are checked by anyone.
- A final effective date for the terms.

## Project privacy draft

`privacy_policy.md` at the Flutter repository root is a draft dated 12 August 2026. It names Akram Mousa as the data controller and matches the app on Google sign-in, profile fields, selected regions rather than GPS, match details, FCM, guest mode, and the absence of in-app card payments and third-party ads.

The same file says to confirm it before publishing a public URL. Two items in it were not used as public facts:

- The contact phone in section 12 is `01097066403`. That number appears in profile unit tests, not in `AppConstants.supportPhone`. The website uses `+20 101 926 0479`.
- “We do not sell personal information”, backup retention for “a limited period”, and the under-13 rule are statements in the draft. The mobile client does not enforce an age gate and does not show backup timing.

## Privacy practices requiring confirmation

- The approved policy text, if one already exists in `GET api/policies`.
- Server-side uses of profile, match, report, and notification data.
- Hosting, backups, access control, and encryption at rest.
- Whether production traffic is HTTPS only. The client base URL is HTTPS, while Android cleartext and iOS arbitrary loads are enabled.
- Retention periods.
- Whether a person can obtain a full export of their data.
- How children’s data should be handled. The client has no account age gate.
- What Google and Firebase retain for sign-in and messaging beyond what this app controls.

## Account deletion details requiring confirmation

Confirmed in the client:

- Signed-in path: Profile → Settings → Account → Delete Account.
- Dialog title and message from `confirm_delete_account` and `delete_account_message`.
- Request: `DELETE api/users/me`.
- Success clears the session, revokes Google access for the app, and shows `delete_account_success`.
- Guests do not see the control.

Not confirmed:

- Which server records are deleted.
- Whether backups, logs, reports, or notification tokens remain.
- Why any record would be kept, and for how long.
- How an email request is matched to an account without a password.
- How long an email request takes.
- The email path is support contact only. It is not the same as the in-app deletion call.

## Missing assets

- No Apple App Store URL. The button stays disabled until `appStoreUrl` is set.
- No approved “Last updated” date for privacy or terms.
- Facebook uses the Yalla Match profile at https://www.facebook.com/profile.php?id=61593627575914. LinkedIn remains Akram Mousa’s developer profile.
- No app screenshots were available to place beside the hero.
- `sitemap.xml` and `robots.txt` still contain `YOUR_GITHUB_USERNAME` and `YOUR_REPOSITORY_NAME` until the public URL exists.

## Incomplete integrations

- The contact form only opens a `mailto` draft. It does not create a ticket.
- Canonical, hreflang, and Open Graph image links are relative until `siteOrigin` is set. Social networks usually want an absolute image URL after the site is public.
- The in-app privacy document is remote. This website cannot show it until the owner provides the approved text.

## Assumptions

- The light theme is the right public look for a support site.
- `#334155`, already a slate in `AppColors`, is used for long paragraphs so body text stays readable. Captions still use the app’s secondary grey.
- Tajawal may be used on the web because the font name table says it is licensed under the SIL Open Font License 1.1.
- The Facebook profile titled Yalla Match is the public Facebook contact. LinkedIn is the developer profile, not a separate company page.
- “Nearby” in the marketing steps follows the app’s own “Nearby Matches” label, while the FAQ explains the real filter behavior.
- A support email is a reasonable fallback when someone cannot finish in-app deletion. It does not by itself delete the account.

## Flutter files inspected

- `pubspec.yaml`
- `lib/core/utils/app_colors.dart`
- `lib/core/utils/app_string.dart`
- `lib/core/utils/endpoint.dart`
- `lib/core/utils/app_dialogs.dart`
- `lib/core/constants.dart`
- `lib/core/theme/theme_light.dart`
- `lib/core/theme/theme_dark.dart`
- `lib/core/network/token_storage.dart`
- `lib/core/network/auth_interceptor.dart`
- `lib/core/services/push_notification_service.dart`
- `lib/core/widgets/custom_app_header.dart`
- `lib/features/auth/data/google_auth_service.dart`
- `lib/features/auth/data/repo/auth_repository.dart`
- `lib/features/auth/presentation/screens/login_screen.dart`
- `lib/features/auth/presentation/widgets/login_logo.dart`
- `lib/features/base/presentation/screens/base_screen.dart`
- `lib/features/base/presentation/widgets/custom_bottom_nav_bar.dart`
- `lib/features/create_match/data/models/create_booking_request.dart`
- `lib/features/create_match/presentation/utils/create_match_validator.dart`
- `lib/features/home/presentation/utils/home_ui.dart`
- `lib/features/match/presentation/widgets/match_details_body.dart`
- `lib/features/policies/data/models/policy_model.dart`
- `lib/features/policies/data/repo/policies_repo.dart`
- `lib/features/profile/data/models/profile_model.dart`
- `lib/features/profile/data/models/update_profile_request.dart`
- `lib/features/profile/data/models/delete_account_response.dart`
- `lib/features/profile/data/data_sources/profile_remote_data_source.dart`
- `lib/features/profile/presentation/manager/settings_cubit.dart`
- `lib/features/profile/presentation/widgets/settings_screen_body.dart`
- `lib/features/profile/presentation/widgets/profile_menu_list.dart`
- `lib/features/profile/presentation/widgets/help_center_contact_section.dart`
- `lib/features/profile/presentation/utils/help_center_contact.dart`
- `assets/i18n/en.json`
- `assets/i18n/ar.json`
- `android/app/src/main/AndroidManifest.xml`
- `ios/Runner/Info.plist`
- `privacy_policy.md`
