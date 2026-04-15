/**
 * PE Collective Newsletter Signup Worker
 *
 * Shares the same Resend audience as AI Pulse (aimarketpulse).
 * Signups from pecollective.com go to the AI Pulse subscriber list.
 *
 * Endpoints:
 *   POST /          — Add contact to Resend audience (signup)
 *   GET  /unsubscribe?email=...  — Unsubscribe contact
 *
 * Secrets (set via `wrangler secret put`):
 *   RESEND_API_KEY
 *
 * Env vars (in wrangler.toml):
 *   RESEND_AUDIENCE_ID
 *   ALLOWED_ORIGIN
 */

const RESEND_API = "https://api.resend.com";

function corsHeaders(origin, allowedOrigin) {
  const allowed = origin === allowedOrigin || origin === "null";
  return {
    "Access-Control-Allow-Origin": allowed ? origin : allowedOrigin,
    "Access-Control-Allow-Methods": "POST, GET, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
  };
}

function jsonResponse(body, status, origin, allowedOrigin) {
  return new Response(JSON.stringify(body), {
    status,
    headers: {
      "Content-Type": "application/json",
      ...corsHeaders(origin, allowedOrigin),
    },
  });
}

async function handleSignup(request, env) {
  const origin = request.headers.get("Origin") || "";
  const allowed = env.ALLOWED_ORIGIN;

  try {
    const { email } = await request.json();
    if (!email || !email.includes("@")) {
      return jsonResponse({ error: "Valid email required" }, 400, origin, allowed);
    }

    const res = await fetch(`${RESEND_API}/audiences/${env.RESEND_AUDIENCE_ID}/contacts`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${env.RESEND_API_KEY}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        email: email.trim().toLowerCase(),
        unsubscribed: false,
        first_name: "pecollective",
      }),
    });

    const data = await res.json();

    if (!res.ok) {
      return jsonResponse({ error: data.message || "Signup failed" }, res.status, origin, allowed);
    }

    return jsonResponse({ success: true }, 200, origin, allowed);
  } catch (e) {
    return jsonResponse({ error: "Invalid request" }, 400, origin, allowed);
  }
}

async function handleUnsubscribe(request, env) {
  const url = new URL(request.url);
  const email = url.searchParams.get("email");

  if (!email || !email.includes("@")) {
    return new Response(unsubPage("Invalid email address.", false), {
      status: 400,
      headers: { "Content-Type": "text/html" },
    });
  }

  try {
    const listRes = await fetch(
      `${RESEND_API}/audiences/${env.RESEND_AUDIENCE_ID}/contacts?email=${encodeURIComponent(email)}`,
      { headers: { Authorization: `Bearer ${env.RESEND_API_KEY}` } }
    );

    let contactId = null;
    if (listRes.ok) {
      const listData = await listRes.json();
      const contacts = listData.data || [];
      const match = contacts.find(c => c.email.toLowerCase() === email.toLowerCase());
      if (match) contactId = match.id;
    }

    if (!contactId) {
      return new Response(unsubPage("You've been unsubscribed.", true), {
        status: 200, headers: { "Content-Type": "text/html" },
      });
    }

    const updateRes = await fetch(
      `${RESEND_API}/audiences/${env.RESEND_AUDIENCE_ID}/contacts/${contactId}`,
      {
        method: "PATCH",
        headers: {
          Authorization: `Bearer ${env.RESEND_API_KEY}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ unsubscribed: true }),
      }
    );

    if (updateRes.ok) {
      return new Response(unsubPage("You've been unsubscribed.", true), {
        status: 200, headers: { "Content-Type": "text/html" },
      });
    }
    return new Response(unsubPage("Something went wrong. Email rome@getprovyx.com.", false), {
      status: 500, headers: { "Content-Type": "text/html" },
    });
  } catch (e) {
    return new Response(unsubPage("Something went wrong. Email rome@getprovyx.com.", false), {
      status: 500, headers: { "Content-Type": "text/html" },
    });
  }
}

function unsubPage(message, success) {
  const color = success ? "#4ade80" : "#f87171";
  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Unsubscribe - PE Collective</title>
  <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;600&display=swap" rel="stylesheet">
  <style>
    body { margin:0; background:#0f2d35; color:#fff; font-family:'DM Sans',sans-serif; display:flex; align-items:center; justify-content:center; min-height:100vh; text-align:center; padding:24px; }
    .card { background:#132f38; border:1px solid rgba(255,255,255,0.1); border-radius:16px; padding:48px 40px; max-width:440px; }
    .icon { font-size:48px; margin-bottom:16px; }
    h1 { font-size:20px; margin:0 0 12px; color:${color}; }
    p { font-size:15px; color:#a8c5cc; line-height:1.6; margin:0; }
    a { color:#e8a87c; text-decoration:none; }
    a:hover { text-decoration:underline; }
  </style>
</head>
<body>
  <div class="card">
    <div class="icon">${success ? "&#x2713;" : "&#x26A0;"}</div>
    <h1>${message}</h1>
    <p>${success
      ? 'You won\'t receive any more emails from AI Pulse.<br><br><a href="https://pecollective.com">Back to pecollective.com</a>'
      : '<a href="https://pecollective.com">Back to pecollective.com</a>'
    }</p>
  </div>
</body>
</html>`;
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const origin = request.headers.get("Origin") || "";

    if (request.method === "OPTIONS") {
      return new Response(null, {
        status: 204,
        headers: corsHeaders(origin, env.ALLOWED_ORIGIN),
      });
    }

    if (url.pathname === "/unsubscribe") {
      return handleUnsubscribe(request, env);
    }

    if (request.method === "POST" && (url.pathname === "/" || url.pathname === "")) {
      return handleSignup(request, env);
    }

    return new Response("Not found", { status: 404 });
  },
};
