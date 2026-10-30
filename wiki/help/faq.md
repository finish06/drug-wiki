# FAQ and troubleshooting

## I get `401 unauthorized`

- `API key required`: the `X-API-Key` header is missing. Check the header name
  is spelled exactly and that your HTTP client actually sends it.
- `Invalid API key`: the key is wrong, deactivated, or past its rotation grace
  period. Request a new one ([API keys](../get-started/api-keys.md)).

## It works with curl but fails in the browser (CORS, "403")

Your website's origin isn't on the key's allowed list, so the browser blocks the
response. The API doesn't send a 403; the browser shows a CORS error. Ask for
your exact origin (scheme + host + port, e.g. `https://myapp.example.com`) to be
added. Keys meant for servers usually have no origins and can't be used from a browser.

## I get `429 rate_limited`

You've used your key's requests for this minute. Wait the `Retry-After` seconds.
Cache results, debounce autocomplete, or ask for a higher limit. See
[Errors and rate limits](../reference/errors.md#rate-limits).

## I get `502 upstream_error`

The API couldn't reach a government data source and had no cached copy. These
are usually brief: retry with backoff (1s, 2s, 4s). Persistent 502s on one
endpoint are worth reporting.

## My NDC isn't found

- Use the **product** NDC with dashes, e.g. `00069-3150` or `0069-3150`.
- Leading zeros matter; don't strip them.
- Products that were discontinued or never listed with the FDA won't be found.
  Try [`/v1/drugs/rxnorm/search`](../guides/rxnorm.md) by name instead.

## The info card has empty sections

The newest label for that name is likely an over-the-counter "Drug Facts" label,
which doesn't use the numbered prescription sections. Use
[`/v1/drugs/spls?name=`](../guides/product-labels.md) to pick a prescription label and fetch it by set ID.

## A misspelled name returns nothing

`/v1/drugs/autocomplete` and `/v1/drugs/info` match names literally. Run the
input through [`/v1/drugs/rxnorm/search`](../guides/rxnorm.md) first: it returns
the closest matches and spelling suggestions.

## Can I use this for clinical decisions?

No. It republishes FDA label text and NLM terminology to help people find
information. The interaction check matches label text and can miss clinically
important interactions.

## Who do I ask?

[Open an issue]({{ key_request_url }}) for keys, limits or bugs.
