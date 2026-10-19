# Notes for Claude

## Business
Meddy Baraei is a Regional / Division Sales Director at Regency Management Services, LLC (dba Ashley), a multi-unit home furniture retailer based in Sterling, Northern Virginia.

## Google Gemini API
Google Gemini API access is connected only in the cloud environment named **"Google -API-key"** (host `generativelanguage.googleapis.com`). There, the network proxy adds the key to requests, so no API key is needed in code or chat, and no `GEMINI_API_KEY` variable exists. Billing is enabled.

Sessions in other environments (such as "Default") have no key, and Google rejects requests with "unregistered caller". If that happens, tell the user to start a new session in the "Google -API-key" environment, or to add the Google key to the current environment's network settings.

- Images: `gemini-3.1-flash-image` (about $0.07 per standard 1K image). Send `"generationConfig": {"responseModalities": ["IMAGE", "TEXT"]}` and decode the base64 `inlineData` from the response.
- Text: `gemini-3.5-flash`.
- Do not put Ashley or other brand logos or names in generated images.
- "Gemini" alone may also refer to the Gemini crypto exchange connector, which is unrelated. Use the Google Gemini API for AI tasks.

Example:

```bash
curl -sS "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-image:generateContent" \
  -H "Content-Type: application/json" \
  -d '{"contents":[{"parts":[{"text":"<prompt>"}]}],"generationConfig":{"responseModalities":["IMAGE","TEXT"]}}'
```
