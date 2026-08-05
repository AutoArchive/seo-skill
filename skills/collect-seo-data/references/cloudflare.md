# Cloudflare analytics collection

## Preferred tool path

Discover tools at runtime because MCP tool names and schemas can change.

1. Prefer `https://graphql.mcp.cloudflare.com/mcp`.
2. Fall back to the official general server at
   `https://mcp.cloudflare.com/mcp` and its GraphQL support.
3. If MCP is unavailable but an authorized API client exists, POST a read-only
   query to `https://api.cloudflare.com/client/v4/graphql`.
4. Otherwise mark Cloudflare blocked. Never request or expose a token in Git.

Official MCP inventory:
<https://github.com/cloudflare/mcp-server-cloudflare>

Official GraphQL Analytics overview:
<https://developers.cloudflare.com/analytics/graphql-api/>

## Zone and query

Use the zone hostname in `site.md`. Require one exact zone match and keep its ID
only in ephemeral tool arguments. Prefer the current
`httpRequestsAdaptiveGroups` dataset. Query the normalized UTC window and use
`requestSource: "eyeball"` for end-user traffic when available.

A baseline aggregate can request request count, `sum.visits`,
`sum.edgeResponseBytes`, and `avg.sampleInterval`. Add dimensions only when
needed and available to the plan. Keep raw grouped rows external. Introspect the
schema because dataset availability and retention vary by account plan.

Current adaptive-groups guidance:
<https://developers.cloudflare.com/analytics/graphql-api/migration-guides/graphql-api-analytics/>

## Correctness and mutation boundary

- Inspect GraphQL `errors` even when HTTP status is 200.
- Confirm exactly one zone and the complete time window.
- Record sampling metadata and the source watermark.
- Respect node, account, zone, history, field, record, and rate limits.
- Never use collection as authorization to change DNS, cache, rules, Workers,
  Pages, WAF, Access, or account settings.

Limits:
<https://developers.cloudflare.com/analytics/graphql-api/limits/>

Error behavior:
<https://developers.cloudflare.com/analytics/graphql-api/errors/>
