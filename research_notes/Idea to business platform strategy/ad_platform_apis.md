# Ad Platform APIs for a Multi-Customer SMB Ad-Management Platform (US, as of Oct 2026)

Research note: direct page fetches to developers.google.com, developers.meta.com and ppc.land failed (DNS errors in the research sandbox), so most findings come from search-result summaries of those pages. Citations point to the underlying pages. Where only a third-party blog was found, it is labelled as such. Items marked "(background knowledge, unverified)" in Inferences are from prior knowledge and were not confirmed in this session.

## Google Ads API: access levels, application, MCC, limits, RMF, billing, campaign-type support, LSA

### Takeaway
In September 2026 Google retired developer tokens. Access levels (Test, Explorer, Basic, Standard) now attach to the Google Cloud project, and new Basic or Standard applications require brand verification. Basic access is now approved automatically within minutes; Standard still gets a manual review. Search, PMax, Demand Gen and AI Max are well supported in the API. Local Services Ads campaigns cannot be created through the API (status, budget and bidding edits only). A third-party platform should run an MCC manager account linked to customer-owned accounts, and Standard-access tools are bound by Required Minimum Functionality (RMF).

### Cited Findings
- **Developer tokens retired:** tokens were sunset on September 9, 2026. Each token's access level moved automatically to the Google Cloud project, based on API activity in the 90 days before the sunset. Some secondary sources date the blog post September 10. — [Google: Developer token](https://developers.google.com/google-ads/api/docs/api-policy/developer-token); [Relevant Audience](https://www.relevantaudience.com/google-ads-en/google-ads-api-developer-tokens-sunset-cloud-project-access/); [Paid Media Collective](https://paidmediacollective.com/newsfeed/google-ads-api-cloud-project-access-2026)
- **Access lives on the Cloud project:** the four levels (Test, Explorer, Basic, Standard) belong to the Google Cloud project that owns the OAuth client or service account. The developer-token header is now optional and ignored, and a future major version is expected to reject it. — [Relevant Audience](https://www.relevantaudience.com/google-ads-en/google-ads-api-developer-tokens-sunset-cloud-project-access/); [Climent Media](https://climentmedia.com/learn/google-ads-api-access/)
- **Brand verification:** new Basic and Standard applications require brand verification. Existing holders are encouraged but not required to verify. — [Google: Developer token](https://developers.google.com/google-ads/api/docs/api-policy/developer-token); [ppc.land](https://ppc.land/google-drops-developer-tokens-from-ads-api-access-decisions/)
- **Basic approval timing:** Basic applications are now automated and reviewed within minutes of brand verification and submission. All Basic applications pending at the changeover were closed and had to be resubmitted. Standard still gets a manual review. — [ppc.land](https://ppc.land/google-drops-developer-tokens-from-ads-api-access-decisions/); [Relevant Audience](https://www.relevantaudience.com/google-ads-en/google-ads-api-developer-tokens-sunset-cloud-project-access/)
- **Known issue:** projects with newly approved Basic or Explorer access have been getting AUTHORIZATION_ERROR. Separately, v25 returns CLOUD_PROJECT_NOT_APPROVED_FOR_PRODUCTION when a Test-level project calls a production account. — [Google: Developer token](https://developers.google.com/google-ads/api/docs/api-policy/developer-token); [mediovsky](https://mediovsky.com/google-ads-api-access/)
- **Explorer Access:** this tier was introduced in October 2025 and broadly launched around February 2026. It reaches production accounts but is capped at 2,880 operations per day. It blocks some functions, including creating client accounts and billing services. Google may grant it automatically, without an application. — [Google Ads Developer Blog, Oct 2025](https://ads-developers.googleblog.com/2025/10/explorer-access-is-now-available-for.html?m=1); [Google: Access levels](https://developers.google.com/google-ads/api/docs/access-levels?hl=en)
- **Basic Access limits:** 15,000 operations per day on test and production accounts. The older documented review time was 2 or 5 business days, depending on the page version. — [Google: Access levels](https://developers.google.com/google-ads/api/docs/access-levels?hl=en)
- **February 2026 backlog:** on February 6, 2026 Google acknowledged significant delays in reviewing token applications and said it had added reviewers. It attributed the surge to the Explorer launch, its MCP server and its Developer Assistant. — [ppc.land](https://ppc.land/google-faces-developer-token-application-backlog-as-new-api-tier-debuts/)
- **RMF scope:** RMF has three groups: creation, management and reporting.
  - A "full-service tool" that third parties use to manage their accounts must offer all three.
  - A reporting-only tool needs reporting only. An internal-only tool is exempt.
  - RMF applies only to Standard Access.
  - The API may only be used as described in the application. Changes need the Tool Change Form.

  — [Google: RMF](https://developers.google.com/google-ads/api/docs/api-policy/rmf); [Google Ads API policies](https://support.google.com/adspolicy/answer/6169371)
- **Production setup:** applicants select or create a Google Ads manager account (MCC) as part of production setup. — [Google: Obtain a developer token](https://developers.google.cn/google-ads/api/docs/get-started/dev-token?hl=en)
- **Consolidated billing:** puts multiple accounts on one monthly invoice under a common "paying manager" MCC. It requires monthly invoicing, which works as a line of credit, and eligibility is typically limited to large advertisers or agencies. Accounts must share a currency, and Manager Defined Spend accounts are incompatible. — [Google: About consolidated billing](https://support.google.com/google-ads/answer/2375371)
- **Current versions and campaign-type support:**
  - v24.2 (June 24, 2026) added Local Services Ads fields on PMax asset groups and a landing-page text-generation enum for Demand Gen video ads.
  - v22 added Demand Gen TargetCPC and asset automation, plus PMax AssetAutomationType values.
  - v21 added an AI Max search term and ad combination report.

  — [Google Ads Developer Blog 2026](https://ads-developers.googleblog.com/2026/?m=0); [seo-day.de](https://www.seo-day.de/news/article/google-ads-api-v242-adds-ai-transparency-stronger-security?lang=en)
- **AI Max (third-party claim):** a third-party post says the API can create AI Max for Search and Shopping campaigns, with some decisions staying under AI control. It cites a "July 2026 ToS" that could not be verified. — [DEV Community](https://dev.to/yositeup/google-ads-api-and-ai-max-automated-campaign-management-at-scale-in-2026-3b2g)
- **LSA creation not supported:** the Google Ads API cannot create or remove Local Services campaigns, and cannot operate on their ad groups, ads or criteria.
- **What the API supports for LSA:**
  - Read campaigns and budgets with channel type LOCAL_SERVICES.
  - Change campaign status and budget.
  - Set bidding (ManualCpa, MaximizeConversions), ad schedule, location targeting and service types.
  - Rate leads through ProvideLeadFeedback.
  - Read lead, conversation, verification and employee reports.

  — [Google: Local Services campaigns](https://developers.google.com/google-ads/api/docs/campaigns/local-service-campaigns?authuser=9)

### Inferences
- **Account model:** the platform should own one MCC, create or link customer-owned Google Ads accounts under it, and have each customer accept the link. Creating client accounts under the MCC requires at least Basic access, because Explorer blocks account creation. (Account creation via CustomerService.CreateCustomerClient is background knowledge, unverified.)
- **Access path:** start with Explorer or Basic, which is now fast once the brand is verified. Apply for Standard before passing about 15,000 operations per day, and once Standard is granted, budget for full RMF compliance.
- **LSA:** onboarding is effectively manual. The business creates the LSA profile and passes background and license checks in the LSA UI. The platform can then manage budget, bidding and status, and pull leads. A newer option is LSA inventory inside PMax asset groups (v24.2), worth tracking.
- **YouTube and video:** treat Demand Gen (which includes YouTube placements) and PMax as the API route to YouTube inventory. Classic YouTube Video campaigns historically had limited create support in the API. (Background knowledge, unverified for 2026.)

### Gaps
- Could not fetch the live access-levels page to confirm current Standard-access operation limits (historically unlimited operations, with per-request rate limits) or Standard review timelines after the September 2026 change.
- Found no official Google statement on a "reseller" programme for fronting media for SMBs. Consolidated billing and monthly invoicing were the only official mechanisms found. Whether the old Google Ads "Reseller" designation still exists in 2026 is unverified.
- No verified 2026 detail on whether classic YouTube Video campaigns (as opposed to Demand Gen) can be created via the API.

## Meta Marketing API: app review, access tiers, Business Verification, Tech Provider, system users, spend limits, special ad categories, Advantage+, ban risk

### Takeaway
Managing ads for other businesses' ad accounts requires three things: app review approval of `ads_management` (and `ads_read`), Full Access (formerly Advanced Access), and Business Verification. As of May 2026 the access tiers were renamed Limited and Full, and the Full Access threshold dropped to 500 API calls in 15 days. New SMB ad accounts commonly face roughly $50 per day spending limits. Every campaign must declare `special_ad_categories`, with financial products/services mandatory in the US since January 2025.

### Cited Findings
- **Tier renaming:** from May 2026, "Ads Management Standard Access" is now the "Marketing API Access Tier". "Standard Access" became Limited Access and "Advanced Access" became Full Access.
- **Lower threshold:** the qualification threshold for Full Access fell from 1,500 to 500 Marketing API calls in the past 15 days.
- **No code changes:** the permission identifiers are unchanged.

  — [Meta for Developers blog](https://developers.meta.com/blog/updates-to-ads-management-standard-access-feature/)
- **Three gates:** the access tier, App Review for `ads_read`/`ads_management`, and Advanced (Full) Access with Business Verification. Limited/Standard access covers only your own accounts, so client accounts need Advanced/Full Access. — [admanage.ai (third-party)](https://admanage.ai/blog/meta-ads-api); [unified.to (third-party)](https://unified.to/blog/how_to_get_your_meta_ads_api_key)
- **Timing:** Business Verification usually takes a few business days. App Review plus verification takes days to weeks. — [unified.to](https://unified.to/blog/how_to_get_your_meta_ads_api_key); [admanage.ai](https://admanage.ai/blog/meta-ads-api)
- **Spending limits on new accounts:**
  - Meta imposes daily spending limits on new business accounts, ad accounts, Pages or apps, and after policy violations or low quality.
  - Limits are commonly about $50 per day for new accounts and rise over time in good standing.
  - There is no easy way to request an increase.
  - The minimum US campaign spending limit is about $100.

  — [Jon Loomer](https://www.jonloomer.com/campaign-spending-limits-account-spending-limits-daily-spending-limits/); [Jon Loomer glossary](https://www.jonloomer.com/glossary/daily-spending-limit/)
- **Special ad categories:**
  - All Marketing API users must state whether new or edited campaigns are in a Special Ad Category: housing, employment, financial products and services, or issues/elections/politics. Other campaigns send NONE or an empty array.
  - FINANCIAL_PRODUCTS_SERVICES replaced CREDIT and has been mandatory for US advertisers or US audiences since January 14, 2025.
  - The official docs were last updated May 21, 2026.

  — [Meta: Special Ad Category](https://developers.facebook.com/documentation/ads-commerce/marketing-api/audiences/special-ad-category)
- **Restricted targeting:** in special categories, age, gender, ZIP code, exclusion targeting, lookalikes and saved audiences are restricted in the US. — [conductatlas (secondary)](https://conductatlas.com/platform/meta/meta-special-ad-category-requirements/)
- **Customer-list restrictions dropped:** the v22.0 changelog says previously announced restrictions on customer-list custom audiences for housing, employment and financial ads will not proceed. — [Meta v22.0 changelog](https://developers.facebook.com/documentation/ads-commerce/marketing-api/marketing-api-changelog/version22.0)
- **Monthly invoicing:** Meta's monthly invoicing is a credit line applied for in Business Suite, with invoices paid within 30 days. Blogs report Meta began requiring some accounts to move to invoicing or direct debit from April 1, 2026, with no published threshold. — [aimerce (third-party)](https://www.aimerce.ai/blogs/what-is-meta-ads-monthly-invoicing); [adsuploader (third-party)](https://adsuploader.com/blog/meta-ads-monthly-invoicing)

### Inferences
- **Customer-owned accounts:** each SMB should own its Business Portfolio and ad account with its own card on file. The platform's Business Manager gets partner access (agency/partner relationship), and API calls run through a platform system user with assigned assets. This keeps billing liability and account-ban blast radius per customer. (System-user and partner-sharing mechanics are background knowledge, unverified here.)
- **Ban risk:** a platform-created batch of brand-new ad accounts with low spend limits, new Pages and automated creative is exactly the profile that triggers Meta integrity restrictions. Mitigations: ramp spend gradually, use verified customer businesses, keep each customer on its own payment method, and avoid recycling assets from banned accounts.
- **SMB verticals:** for verticals like real estate, mortgage, lending, insurance and recruiting, the platform must set `special_ad_categories` correctly, or ads will be rejected and accounts may be flagged.

### Gaps
- No 2026 source was found on the Meta "Tech Provider" programme requirements for Marketing API (it is mostly documented for WhatsApp), or on Meta Business Partner badging.
- No official 2026 documentation was retrieved on Advantage+ campaign API support. Meta moved to a unified "Advantage+" campaign structure in 2025, but the API specifics for 2026 are unverified.
- No quantified data on ad-account ban rates for new SMB accounts.

## TikTok Marketing API, Business Center, approvals; US regulatory status 2026

### Takeaway
TikTok's US regulatory risk is largely resolved: TikTok USDS Joint Venture LLC was established January 22, 2026, ad delivery continued, and forecasts project 27.9% US ad revenue growth in 2026. Marketing API access requires a developer app on the TikTok for Business portal, advertiser OAuth, and app review plus a data-security check for production. Plan for a multi-week approval.

### Cited Findings
- **Joint venture:** TikTok USDS Joint Venture LLC was established January 22, 2026.
  - ByteDance holds about 19.9%. Oracle, Silver Lake and MGX hold about 45-50%; sources differ.
  - US data and the algorithm run in Oracle's US cloud, with the algorithm retrained on US data.

  — [Marketing Dive](https://www.marketingdive.com/news/tiktok-pitches-advertisers-on-bold-new-chapter-under-us-joint-venture/815632/); [elevarus](https://elevarus.com/tiktok-ads-us-deal-advertiser-playbook-2026/); [Code3](https://code3.com/?p=3052)
- **Advertiser outlook:**
  - eMarketer forecasts 27.9% US TikTok ad revenue growth in 2026.
  - Sponsored content volume rose 17% after the deal.
  - eMarketer warns that operational distance from ByteDance's global systems could slow innovation.

  — [eMarketer](https://www.emarketer.com/content/tiktok-sponsored-content-rebounds-quickly-after-us-deal--with-volume-up-17)
- **Separate programmes:** the Marketing API sits in TikTok for Business, not TikTok for Developers. — [TikTok for Developers FAQ](https://developers.tiktok.com/doc/getting-started-faq); [TikTok Ads Help: About API for Business](https://ads.tiktok.com/help/article?aid=11971)
- **Production path:** new apps start in Sandbox. Production requires app review and a data-security compliance check. Business Center is the hub for multiple ad accounts. Plan for a multi-week approval; one guide says up to two weeks. — [unified.to (third-party)](https://unified.to/blog/how_to_get_your_tiktok_ads_api_key); [echotik (third-party)](https://www.echotik.live/blog/is-tiktoks-api-public-access-approval-process-2025/)
- **Symphony:** TikTok announced the Symphony Creative Suite and Symphony Agent, with an API, on June 22, 2026. — [unified.to](https://unified.to/blog/13_advertising_apis_to_integrate_with_in_2026_google_ads_meta_ads_tiktok_ads_and_unified_advertising_apis)

### Inferences
- **Account model:** the platform runs a Business Center, and customers either grant it access to their ad accounts or the platform creates accounts under its Business Center. The second option makes the platform more liable for billing and policy.
- **Creative:** Symphony APIs could reduce the cost of producing video creative for SMBs.

### Gaps
- No official TikTok page detailing 2026 approval timelines or a "Marketing Partner" track.
- No details on whether the API structure or endpoints changed for US advertisers after the joint venture.

## Microsoft Advertising, Pinterest, Snap, LinkedIn, Nextdoor (brief)

### Takeaway
Microsoft is the easiest of these (a developer token from the portal, agency approval within about 5 days), but SOAP is being deprecated. Snap is open. Pinterest and LinkedIn are gated: LinkedIn takes weeks to months. Nextdoor's Ads API is partner-request based, and Nextdoor also runs a Conversions API.

### Cited Findings
- **Microsoft developer token:** requested in the Developer Portal by a Super Admin. Access to client accounts still depends on per-user roles (e.g. Super Admin, Advertiser Campaign Manager). A universal sandbox token exists. — [Microsoft Learn: Get started](https://learn.microsoft.com/en-us/advertising/guides/get-started)
- **Microsoft timing and deprecation:** first-party tokens are often issued instantly, while agency approval takes up to 5 business days. SOAP feature freeze is October 1, 2026 and full shutdown January 31, 2027; this was not verified with Microsoft. — [unified.to (third-party)](https://unified.to/blog/how_to_get_your_microsoft_advertising_api_key)
- **LinkedIn:**
  - The Advertising API is available to developers approved for it via the Marketing Developer Platform.
  - The Standard tier is needed to manage more than 5 ad accounts.
  - Approval is manual: realistically 4 weeks at best and 4 months on average, with a "Technical Sign Off" demo.

  — [Microsoft Learn: LinkedIn Increasing Access](https://learn.microsoft.com/en-us/linkedin/marketing/increasing-access); [Phyllo (third-party)](https://www.getphyllo.com/post/linkedin-api-access-in-2026-partner-program-approval-timeline-alternatives)
- **Pinterest:** a Trial to Standard tier model gates production write access, with a demo video required. — [unified.to (third-party)](https://unified.to/blog/how_to_get_your_snapchat_ads_api_key)
- **Snapchat:** the Marketing API has been open to all advertisers, agencies and developers since February 2018, with OAuth credentials from Snapchat Business Manager. — [unified.to (third-party)](https://unified.to/blog/how_to_get_your_snapchat_ads_api_key)
- **Nextdoor:**
  - The Ads API Program launched in April 2024. It lets businesses and agency partners create, deliver and measure campaigns from their own platforms, and access is requested via the Developer Site.
  - Early partners included Taradel, Boost by Lone Wolf and Unified Enterprises.
  - Nextdoor also offers a Conversions API.

  — [Nextdoor press release](https://about.nextdoor.com/press-releases/nextdoor-launches-ads-api-program-offering-advertisers-an-easier-way-to-extend-their-campaigns-to-nextdoor); [Nextdoor/Taradel blog](https://business.nextdoor.com/en-us/blog/supercharging-local-advertising-taradel-and-nextdoor-partner-to-offer-advertisers-more-hyperlocal-reach)

### Inferences
- **Launch order:** Google, Meta and Microsoft first; Microsoft is a cheap add because Google campaigns can be mirrored to it.
- **Hyperlocal:** Nextdoor is a strong fit for hyperlocal SMBs, but needs a partnership conversation.
- **Lower priority:** LinkedIn's long approval and B2B focus make it low priority for local SMBs.

### Gaps
- No official Pinterest or Snap documentation was retrieved for 2026.
- No current Nextdoor partner terms, minimums or approval timelines found.

## Google Business Profile API

### Takeaway
The Business Profile APIs need a manual access application. Quota stays at 0 QPM until approval, then is 300 QPM. Google says reviews take up to 14 days, but developers report longer silences in 2026.

### Cited Findings
- **Gate and quota:** until Basic API access is approved, quota is 0 QPM and calls fail with 429. An approved project has 300 QPM by default.
- **Review time:** Google's FAQ says requests are reviewed within 14 days.

  — [Google: GBP FAQ](https://developers.google.com/my-business/content/faq); [Google: Usage limits](https://developers.google.com/my-business/content/limits?authuser=1)
- **Eligibility (third-party):** a legitimate use case, a verified GBP active for 60+ days and a valid website are required. The request should come from an owner or manager email. — [unified.to (third-party)](https://unified.to/blog/how_to_set_up_google_business_profile_api_access_and_get_oauth_2_credentials)
- **Delays in practice:** in a July 2026 forum post, a resubmitted application was still at 0 QPM with no response. The earlier rejection was over a website mismatch. — [Google Developer forum](https://discuss.google.dev/t/gbp-api-access-request-no-response-quota-still-0-qpm-after-resubmission/380564)
- **Quota increases:** requested via the GBP API contact form. — [Google: GBP FAQ](https://developers.google.com/my-business/content/faq)

### Inferences
- Apply for GBP API access early, using a business domain whose website matches the application exactly.

### Gaps
- No verified 2026 list of deprecated GBP API features.

## Payments and billing: fronting ad spend vs card-on-file; chargeback risk

### Takeaway
The only official consolidated-billing routes found are Google consolidated billing (monthly invoicing on a paying-manager MCC, mainly for established agencies) and Meta monthly invoicing (a credit line). A startup will almost certainly not qualify at launch. The practical model is customer-owned accounts with the customer's own card on file at each platform, while the platform bills only its service fee.

### Cited Findings
- **Google:** consolidated billing requires a paying manager account and monthly invoicing (a line of credit). Eligibility is typically limited to larger advertisers and agencies, with an agency managing client accounts given as the example. — [Google: About consolidated billing](https://support.google.com/google-ads/answer/2375371)
- **Meta:** monthly invoicing is a credit line paid within 30 days, and the eligibility threshold is unpublished. — [aimerce (third-party)](https://www.aimerce.ai/blogs/what-is-meta-ads-monthly-invoicing)
- **Explorer restriction:** Explorer Access blocks billing services, so programmatic billing setup needs Basic or above. — [Google: Access levels](https://developers.google.com/google-ads/api/docs/access-levels?hl=en)

### Inferences
- **Credit and fraud exposure of fronting spend:** if the platform fronts media (charges customers, pays platforms on its own card or credit line), it takes on credit risk. It also risks chargebacks of up to 120 days on card networks while the media is already spent and non-refundable, and fraudsters using the platform as a laundering front. One fraudulent customer can also put the platform's shared billing account and MCC at risk. (Reasoned inference; no source found quantifying this.)
- **Recommended setup:** customer card on file in the customer's own ad accounts, platform fee via Stripe. Revisit invoicing and reseller status after reaching scale and agency-partner status.

### Gaps
- No source found on the 2026 status of Google's "Third-party partner / reseller" programme or Meta's reseller/agency credit-line requirements.
- No data found on chargeback rates in ad-spend reselling.

## Tracking: Meta CAPI, Google enhanced conversions, offline conversion import, call tracking

### Takeaway
Server-side conversion signals are needed to optimise campaigns for SMBs with offline sales (calls, appointments). The relevant mechanisms are Meta CAPI, Google enhanced conversions and offline/lead conversion import, LSA lead feedback, and Nextdoor CAPI. Only limited sourcing was found this session.

### Cited Findings
- **LSA:** the Google Ads API supports LSA lead feedback (ProvideLeadFeedback) and lead/conversation reporting. — [Google: Local Services campaigns](https://developers.google.com/google-ads/api/docs/campaigns/local-service-campaigns?authuser=9)
- **Nextdoor:** offers a Conversions API for online and offline conversions. — [Nextdoor press release](https://about.nextdoor.com/press-releases/nextdoor-launches-ads-api-program-offering-advertisers-an-easier-way-to-extend-their-campaigns-to-nextdoor)

### Inferences
- **Components to build** (background knowledge, unverified for 2026):
  - A per-customer pixel plus server-side CAPI relay with deduplication via event_id.
  - Google enhanced conversions for web and leads (hashed email/phone).
  - Offline click conversion upload of GCLID or hashed identifiers from the CRM.
  - Call tracking with dynamic number insertion that posts qualified calls back as conversions.

### Gaps
- Did not retrieve 2026 docs on Meta CAPI requirements, Google enhanced conversions for leads, or Google's 2025-26 changes to offline conversion import (e.g. the shift to Data Manager API). These need verification.

## Practical risks: suspensions, policy, "circumventing systems"

### Takeaway
The biggest operational risks are (1) a bad customer harming the platform's shared MCC, Business Manager or app standing, (2) new-account spend caps and integrity reviews on Meta, (3) wrong special-ad-category declarations, and (4) using the API outside the use declared in the application (Google requires a Tool Change Form).

### Cited Findings
- **Declared use:** Google requires API use to match the application, with changes via the Tool Change Form. — [Google: RMF](https://developers.google.com/google-ads/api/docs/api-policy/rmf)
- **Meta spend limits:** applied after policy violations or low ad quality. — [Jon Loomer](https://www.jonloomer.com/campaign-spending-limits-account-spending-limits-daily-spending-limits/)
- **Meta categories:** Meta requires every API campaign to declare a special ad category. — [Meta: Special Ad Category](https://developers.facebook.com/documentation/ads-commerce/marketing-api/audiences/special-ad-category)

### Inferences
- **"Circumventing systems":** Google's policy covers creating new accounts to evade a suspension, and linked suspended accounts can cascade to the MCC and to other accounts sharing payment or identity. The platform needs KYC on customers, vertical screening (e.g. locksmiths, garage door services and other high-fraud local services that Google restricts), and must never recreate accounts for suspended customers. (Background knowledge, unverified in this session.)

### Gaps
- No 2026 source retrieved on Google's MCC-level suspension cascade rules or Meta's partner-level enforcement.

## Middleware and aggregators to build on

### Takeaway
"Unified ads API" vendors exist and claim write support across major platforms: Unified.to (writes on 15 of 19 integrations) and Zernio (paid campaigns on 8 platforms). Coverage is shallow (pause, budget) compared with native APIs, and the claims are vendor marketing. Native integration is still needed for Google and Meta campaign creation.

### Cited Findings
- **Unified.to:** added an Advertising category in January 2026, covering Google, Meta and TikTok for reads. By July 2026 it claimed writes such as pausing and budget changes. Its write surface is 77 properties across 5 objects on 15 of 19 integrations, including LinkedIn, Microsoft, Amazon, Pinterest, Reddit, Snapchat and X. — [Unified.to blog](https://unified.to/blog/best_unified_api_for_advertising_in_2026); [Unified.to docs](https://docs.unified.to/ads/overview)
- **Zernio:** claims paid campaign management across 8 platforms (Meta, Google, TikTok, LinkedIn, Pinterest, X, ChatGPT). Its ranking of itself as the top pick is self-promotional. — [Zernio](https://zernio.com/blog/best-universal-ads-apis)

### Inferences
- **Build vs buy:** use an aggregator for reporting and simple controls on tail platforms. Build native Google and Meta integrations, because RMF, PMax and Advantage+ structures, and special categories need full API depth. Note that an aggregator does not remove the need for each platform's own app approval in many cases, or for the customer's OAuth consent.

### Gaps
- No verified 2026 information on Hunch, Smartly, Madgicx or Birch API offerings for third-party builders. These are mostly SaaS UIs aimed at advertisers, not white-label APIs. Pricing for the unified-API vendors was not found.
