# Quickstart

Your first successful request in about five minutes.

**You need:** an API key ([get one](api-keys.md)) and a terminal or code editor.

## 1. Save your key

```bash
export DRUG_API_KEY="pk_your_key_here"
```

## 2. Ask for a drug's label information

This asks for warfarin's info card: the newest FDA label, with its
interactions, contraindications, warnings and adverse reactions.

=== "curl"

    ```bash
    curl -s "{{ api_base }}/v1/drugs/info?name=warfarin" \
      -H "X-API-Key: $DRUG_API_KEY"
    ```

=== "JavaScript"

    ```javascript
    const res = await fetch("{{ api_base }}/v1/drugs/info?name=warfarin", {
      headers: { "X-API-Key": process.env.DRUG_API_KEY },
    });
    if (!res.ok) throw new Error(`${res.status}: ${(await res.json()).message}`);
    const info = await res.json();
    console.log(info.spl.title, info.interactions.length, "interaction sections");
    ```

=== "Python"

    ```python
    import os, requests

    res = requests.get(
        "{{ api_base }}/v1/drugs/info",
        params={"name": "warfarin"},
        headers={"X-API-Key": os.environ["DRUG_API_KEY"]},
        timeout=30,
    )
    res.raise_for_status()
    info = res.json()
    print(info["spl"]["title"], len(info["interactions"]), "interaction sections")
    ```

## 3. Check the response

You should get `200` and JSON like this (text shortened):

```json
{
  "drug_name": "warfarin",
  "input_type": "name",
  "input_value": "warfarin",
  "spl": {
    "title": "WARFARIN SODIUM TABLET [SUN PHARMACEUTICAL INDUSTRIES, INC.]",
    "setid": "8ad881e0-ca41-42ad-9d7d-eb85b3a30af0",
    "published_date": "Oct 26, 2026",
    "spl_version": 15
  },
  "interactions": [
    { "title": "7 DRUG INTERACTIONS", "text": "Concomitant use of drugs that increase bleeding risk, …" }
  ],
  "contraindications": [ { "title": "4 CONTRAINDICATIONS", "text": "…" } ],
  "warnings": [ { "title": "5 WARNINGS AND PRECAUTIONS", "text": "…" } ],
  "adverse_reactions": [ { "title": "6 ADVERSE REACTIONS", "text": "…" } ]
}
```

Got something else?

| You got | Why | Fix |
|---|---|---|
| `401 unauthorized` | Missing or wrong key | Check the `X-API-Key` header and the key's value |
| `429` | Over your per-minute limit | Wait `Retry-After` seconds |
| CORS error in the browser | Your site's origin isn't on the key | Ask for it to be added ([API keys](api-keys.md#using-the-key-from-a-browser-vs-a-server)) |
| `502 upstream_error` | A data source was unreachable | Retry shortly ([FAQ](../help/faq.md)) |

## Next

- Pick a guide from [Start here](../index.md#i-want-to) for what you're building.
- Browse [All endpoints](../reference/endpoints.md).
- Try requests in the browser with the [interactive API](../reference/api.md).
