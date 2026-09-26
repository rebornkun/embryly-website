# Embryly website preview — September 26, 2026

This is an uncommitted preview. No production deployment, policy activation, GitHub commit, or App Store submission is authorized yet.

## Implementation evidence

App reviewed at `/Users/benedictshogunle/Documents/ChatGPT/embryly`.

- `supabase/functions/_shared/meal-catalog.ts`: deterministic catalog eligibility/ranking; pregnancy week, preferences, allergens, cultural preferences, variety and recent matches. Lower carbohydrate is ranking; halal/kosher select plant based ideas without certification. Some unsupported/contradictory restrictions produce no match. No universal availability claim.
- `supabase/migrations/202609190002_publish_wellness_catalog.sql`: automated editorial publication; clinical approval and kitchen testing false. References CDC, FoodSafety.gov, NHS, USDA.
- `data/meal-catalog/sources.json`: FDA fish guidance and USDA SR Legacy nutrient provenance. AI ingredient matching and estimates are not measured or clinical values.
- `supabase/functions/analyze-scan/index.ts`: OpenAI GPT-4o API for scans; Open Food Facts barcode lookup. Profile health/preferences, week, nutrient summary and weight can be included. Sensitive context is logged. No benchmark found.
- `src/app/(onboarding)/food-guidance.tsx`: legacy “Up to 90% accuracy” marketing, not evidence of accuracy. Website does not claim a percentage.
- `src/services/food-log.service.ts`: uploads user images to food-images and obtains public URLs. Images can be associated with shared foods. Private access cannot be promised.
- `supabase/migrations/013_soft_delete_account.sql`: account soft deletion, 30 day restoration, no automatic hard deletion. Website describes this explicitly and gives an erasure request route.
- `src/app/(onboarding)/consent.tsx`: all three wellness/privacy/analytics acknowledgments required. This does not establish separate, freely given explicit health or optional analytics consent.
- `src/utils/logger.ts`: Sentry import commented. No active product analytics SDK established from inspected code.
- `src/constants/paywall.ts`: defaults $9.99 weekly / $34.99 yearly. These are preview defaults, not confirmed App Store offers.
- Existing website identifies Benekan Technologies LLC, info@benekan.com, Illinois / Cook County. Registered address and governing jurisdiction need owner confirmation.

## Must resolve before claiming launch readiness

1. Confirm registered company address, jurisdiction and privacy mailbox; obtain qualified legal review of terms, liability cap, eligibility, consumer rights and international applicability. Disclaimers do not eliminate legal liability or determine medical device status independently of functionality and claims.
2. Remove or substantiate the app’s 90% accuracy statement with a scoped evaluation, test set, denominators, failure cases and date. A confidence score is not accuracy.
3. Implement and verify permanent erasure across database records, uploaded images, auth, derived records, processors and backups; define support verification and retention schedules. Do not promise automatic deletion on day 30.
4. Separate private user uploads from public catalog assets, enforce ownership policies, use signed URLs, prevent shared food records from exposing user images, and test access isolation.
5. Remove sensitive profile/weight/scan content from routine logs, define log access and retention, and verify production configuration.
6. Separate necessary processing from optional analytics consent. Implement specific health-data and third-party AI disclosures/permissions, withdrawal and records; assess GDPR Articles 6 and 9, DPIA, privacy by design and state consumer health requirements. A policy alone is not compliance.
7. Verify processors, production hosting/database regions, subprocessors, DPAs, international transfer mechanisms, EU/UK representation needs and incident response. Assess FTC Health Breach Notification Rule and Washington/other state health privacy scope with counsel.
8. Confirm the real App Store URL and approved prices/trial terms. The current Download app navigation leads to an honest availability section; it is not a fake store button.
9. Confirm canonical production domain before enabling indexing and deploying. Preview is deliberately noindex and robots-disallowed. Publishing requires accurate canonical/social/schema/sitemap URLs and removal of draft labeling after approval.
10. Review public source accuracy and local-country differences; no clinical review is claimed for the two educational articles. No marketing ratings, endorsements or user counts are fabricated.

## Design references

- Lunera: centered hero, floating pill navigation, large phone composition, small floating UI notes.
- Necta: clear feature rhythm and product phone presentation.
- Daylo: quieter editorial typography, numbered progression, generous spacing and rounded content cards. Inspected page text/structure; its hero animation remained on an intro frame during screenshot inspection.

The implementation is original HTML/CSS/JS. No template code or third-party marketing artwork copied.

## Assets and article briefs

Real app captures from `docs/app-store-screenshots` in the app repo use fictional sample data. Nine PNGs converted to 780px JPEGs for website delivery. Meal artwork is existing app catalog art, labeled illustrative in articles.

Article 1: use case / pregnancy food-safety decisions. Query hypothesis “food safety during pregnancy”; no Search Console or measured search volume claimed. Unique value: distinguish food identity from preparation/storage and explain scan limitations. Sources: CDC, FoodSafety.gov, FDA/EPA.
Article 2: use case / flexible pregnancy meal planning. Query hypothesis “pregnancy meal plan”; no measured demand claimed. Unique value: use alternative ideas without implying a prescribed or nutritionally complete day. Sources: NHS and CDC; verified app matching and profile behavior.

## Reference checks

Public sources consulted September 26, 2026:
- https://www.cdc.gov/food-safety/foods/pregnant-women.html
- https://www.cdc.gov/food-safety/prevention/index.html
- https://www.foodsafety.gov/people-at-risk/pregnant-women
- https://www.foodsafety.gov/food-safety-charts/safe-minimum-internal-temperatures
- https://www.fda.gov/food/consumers/advice-about-eating-fish
- https://www.nhs.uk/pregnancy/keeping-well/have-a-healthy-diet/
- https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/lawful-basis/special-category-data/what-are-the-rules-on-special-category-data/
- https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/lawful-basis/consent/what-is-valid-consent/
- https://developers.openai.com/api/docs/guides/your-data
- https://www.ftc.gov/business-guidance/resources/complying-ftcs-health-breach-notification-rule-0
- https://www.atg.wa.gov/protecting-washingtonians-personal-health-data-and-privacy
- https://www.fda.gov/regulatory-information/search-fda-guidance-documents/general-wellness-policy-low-risk-devices

These are research inputs, not legal or medical approval of Embryly.
