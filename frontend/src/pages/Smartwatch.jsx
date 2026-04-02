import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

// ── Google Fit OAuth config ───────────────────────────────────────────────────
const GOOGLE_CLIENT_ID = "951085503109-f69cclagcd7nmqp6jcrvocr631c5jho5.apps.googleusercontent.com";
const FIT_SCOPES = [
  "https://www.googleapis.com/auth/fitness.activity.read",
  "https://www.googleapis.com/auth/fitness.body.read",
  "https://www.googleapis.com/auth/fitness.sleep.read",
  "https://www.googleapis.com/auth/fitness.heart_rate.read",
].join(" ");

// ── Fitbit OAuth config ───────────────────────────────────────────────────────
// Users need to register their own Fitbit app at dev.fitbit.com
// We use implicit grant (token in URL hash) — no backend needed
const FITBIT_CLIENT_ID = ""; // placeholder — user fills in their own

// ── Helpers ───────────────────────────────────────────────────────────────────
const minsToTime = (totalMins) => {
  const h = Math.floor(totalMins / 60) % 24;
  const m = totalMins % 60;
  return `${String(h).padStart(2, "0")}:${String(m).padStart(2, "0")}`;
};

const stepsToActivity = (steps) => {
  if (steps >= 10000) return "Active";
  if (steps >= 5000)  return "Moderate";
  return "Sedentary";
};

// ── Google Fit fetcher ────────────────────────────────────────────────────────
async function fetchGoogleFitData(accessToken) {
  const now = Date.now();
  const weekAgo = now - 7 * 24 * 60 * 60 * 1000;

  const body = {
    aggregateBy: [
      { dataTypeName: "com.google.step_count.delta" },
      { dataTypeName: "com.google.weight" },
      { dataTypeName: "com.google.height" },
      { dataTypeName: "com.google.heart_rate.bpm" },
      { dataTypeName: "com.google.sleep.segment" },
    ],
    bucketByTime: { durationMillis: 7 * 24 * 60 * 60 * 1000 },
    startTimeMillis: weekAgo,
    endTimeMillis: now,
  };

  const res = await fetch(
    "https://www.googleapis.com/fitness/v1/users/me/dataset:aggregate",
    {
      method: "POST",
      headers: {
        Authorization: `Bearer ${accessToken}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify(body),
    }
  );

  if (!res.ok) throw new Error(`Google Fit API error: ${res.status}`);
  const data = await res.json();

  let steps = null, weightKg = null, heightM = null, heartRate = null;
  let sleepMins = null;

  for (const bucket of data.bucket || []) {
    for (const dataset of bucket.dataset || []) {
      const type = dataset.dataSourceId || "";
      for (const point of dataset.point || []) {
        const val = point.value?.[0];
        if (!val) continue;

        if (type.includes("step_count"))
          steps = Math.round(val.intVal || val.fpVal || 0);
        else if (type.includes("weight"))
          weightKg = Math.round((val.fpVal || 0) * 10) / 10;
        else if (type.includes("height"))
          heightM = Math.round((val.fpVal || 0) * 100) / 100;
        else if (type.includes("heart_rate"))
          heartRate = Math.round(val.fpVal || 0);
        else if (type.includes("sleep")) {
          // sum sleep segment durations (type 1 = sleeping)
          if (val.intVal === 1 || val.intVal === 2) {
            const dur = (point.endTimeNanos - point.startTimeNanos) / 1e9 / 60;
            sleepMins = (sleepMins || 0) + dur;
          }
        }
      }
    }
  }

  return { steps, weightKg, heightM, heartRate, sleepMins };
}

// ── Manual import parser ──────────────────────────────────────────────────────
function parseManualJson(text) {
  try {
    const d = JSON.parse(text);
    return {
      steps:     d.steps     || d.step_count || null,
      weightKg:  d.weight_kg || d.weight     || null,
      heightM:   d.height_m  || d.height     || null,
      heartRate: d.heart_rate || d.resting_heart_rate || null,
      sleepMins: d.sleep_minutes || (d.sleep_hours ? d.sleep_hours * 60 : null),
      glucose:   d.glucose   || d.blood_glucose || null,
      bloodPressure: d.blood_pressure || d.systolic || null,
    };
  } catch {
    return null;
  }
}

// ── Map fetched data → Predict form fields ────────────────────────────────────
function mapToFormFields(fetched) {
  const fields = {};

  if (fetched.weightKg) {
    fields.weightVal  = fetched.weightKg;
    fields.weightUnit = "kg";
  }
  if (fetched.heightM) {
    fields.heightVal  = Math.round(fetched.heightM * 100);
    fields.heightUnit = "cm";
  }
  if (fetched.steps) {
    fields.physical_activity = stepsToActivity(fetched.steps);
  }
  if (fetched.sleepMins) {
    // Convert total sleep minutes to bed/wake times (assume wake at 06:30)
    const wakeMinutes = 6 * 60 + 30;
    const bedMinutes  = (wakeMinutes - Math.round(fetched.sleepMins) + 24 * 60) % (24 * 60);
    fields.bedTime  = minsToTime(bedMinutes);
    fields.wakeTime = minsToTime(wakeMinutes);
  }
  if (fetched.glucose)        fields.Glucose       = fetched.glucose;
  if (fetched.bloodPressure)  fields.BloodPressure = fetched.bloodPressure;

  return fields;
}

// ── Source card component ─────────────────────────────────────────────────────
function SourceCard({ icon, name, description, badge, onClick, disabled, children }) {
  return (
    <div className={`p-6 rounded-2xl border transition-all ${disabled ? "border-slate-800 opacity-50" : "border-slate-700 hover:border-emerald-500/40 cursor-pointer"} bg-slate-800/60`}>
      <div className="flex items-start justify-between mb-3">
        <div className="flex items-center gap-3">
          <span className="text-3xl">{icon}</span>
          <div>
            <p className="text-white font-bold">{name}</p>
            <p className="text-slate-400 text-xs mt-0.5">{description}</p>
          </div>
        </div>
        {badge && (
          <span className={`text-xs font-bold px-2 py-1 rounded-full border ${
            badge === "Free" ? "text-emerald-400 border-emerald-500/40 bg-emerald-500/10" :
            badge === "Setup needed" ? "text-yellow-400 border-yellow-500/40 bg-yellow-500/10" :
            "text-slate-400 border-slate-600 bg-slate-700/50"
          }`}>{badge}</span>
        )}
      </div>
      {children}
      {onClick && !disabled && (
        <button
          onClick={onClick}
          className="mt-4 w-full bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold py-2.5 rounded-xl text-sm transition-all"
        >
          Connect {name}
        </button>
      )}
      {disabled && <p className="text-slate-600 text-xs mt-3">Not available in web browsers</p>}
    </div>
  );
}

// ── Main page ─────────────────────────────────────────────────────────────────
export default function Smartwatch() {
  const navigate = useNavigate();
  const { user } = useAuth();

  const [status, setStatus]     = useState(null); // "loading" | "success" | "error"
  const [message, setMessage]   = useState("");
  const [fetched, setFetched]   = useState(null);
  const [manualText, setManualText] = useState("");
  const [showManual, setShowManual] = useState(false);

  // ── Google Fit connect ──────────────────────────────────────────────────────
  const connectGoogleFit = () => {
    const params = new URLSearchParams({
      client_id:     GOOGLE_CLIENT_ID,
      redirect_uri:  window.location.origin + "/smartwatch",
      response_type: "token",
      scope:         FIT_SCOPES,
      include_granted_scopes: "true",
    });
    window.location.href = `https://accounts.google.com/o/oauth2/v2/auth?${params}`;
  };

  // Handle OAuth redirect (token in URL hash)
  useState(() => {
    const hash = window.location.hash;
    if (!hash.includes("access_token")) return;
    const params = new URLSearchParams(hash.slice(1));
    const token  = params.get("access_token");
    if (!token) return;

    // Clean URL
    window.history.replaceState({}, "", "/smartwatch");

    setStatus("loading");
    setMessage("Fetching your health data from Google Fit...");

    fetchGoogleFitData(token)
      .then((data) => {
        setFetched(data);
        setStatus("success");
        setMessage("Data fetched successfully from Google Fit!");
      })
      .catch((err) => {
        setStatus("error");
        setMessage(err.message || "Failed to fetch Google Fit data.");
      });
  });

  // ── Fitbit connect ──────────────────────────────────────────────────────────
  const connectFitbit = () => {
    if (!FITBIT_CLIENT_ID) {
      setStatus("error");
      setMessage("Fitbit Client ID not configured. See instructions below.");
      return;
    }
    const params = new URLSearchParams({
      client_id:     FITBIT_CLIENT_ID,
      redirect_uri:  window.location.origin + "/smartwatch",
      response_type: "token",
      scope:         "activity heartrate sleep weight profile",
      expires_in:    "86400",
    });
    window.location.href = `https://www.fitbit.com/oauth2/authorize?${params}`;
  };

  // ── Manual import ───────────────────────────────────────────────────────────
  const handleManualImport = () => {
    const parsed = parseManualJson(manualText);
    if (!parsed) {
      setStatus("error");
      setMessage("Invalid JSON. Check the format below.");
      return;
    }
    setFetched(parsed);
    setStatus("success");
    setMessage("Data imported successfully!");
  };

  // ── Pre-fill and navigate ───────────────────────────────────────────────────
  const handleUseFetchedData = () => {
    if (!fetched) return;
    const fields = mapToFormFields(fetched);
    // Store in sessionStorage so Predict page can pick it up
    sessionStorage.setItem("smartwatch_prefill", JSON.stringify(fields));
    navigate("/predict");
  };

  const dataRows = fetched ? [
    { label: "Steps (7-day avg)",    value: fetched.steps     ? `${fetched.steps.toLocaleString()} steps/day` : null, icon: "👟" },
    { label: "Weight",               value: fetched.weightKg  ? `${fetched.weightKg} kg` : null,                      icon: "⚖️" },
    { label: "Height",               value: fetched.heightM   ? `${Math.round(fetched.heightM * 100)} cm` : null,     icon: "📏" },
    { label: "Resting Heart Rate",   value: fetched.heartRate ? `${fetched.heartRate} bpm` : null,                    icon: "❤️" },
    { label: "Avg Sleep",            value: fetched.sleepMins ? `${Math.round(fetched.sleepMins / 60 * 10) / 10} hrs` : null, icon: "😴" },
    { label: "Glucose",              value: fetched.glucose   ? `${fetched.glucose} mg/dL` : null,                    icon: "🩸" },
    { label: "Blood Pressure",       value: fetched.bloodPressure ? `${fetched.bloodPressure} mmHg` : null,           icon: "💉" },
  ].filter((r) => r.value) : [];

  return (
    <div className="min-h-screen bg-slate-900 text-slate-100 py-12 px-6">
      <div className="max-w-4xl mx-auto">

        {/* Header */}
        <div className="text-center mb-10">
          <div className="inline-flex items-center gap-2 bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-sm font-semibold px-4 py-1.5 rounded-full mb-4">
            ⌚ Smart Device Integration
          </div>
          <h1 className="text-4xl font-black text-white mb-3">Connect Your Smartwatch</h1>
          <p className="text-slate-400 max-w-xl mx-auto mb-6">
            Pull real health data from your fitness device for a more accurate risk analysis.
            Your data stays in your browser — we never store raw device data.
          </p>

          {/* Compatibility strip */}
          <div className="inline-flex flex-wrap justify-center gap-3 text-xs">
            {[
              { icon: "🤖", label: "Android / Wear OS",   how: "Google Fit",  color: "emerald" },
              { icon: "📱", label: "Fitbit",               how: "Direct API",  color: "emerald" },
              { icon: "⌚", label: "Mi Band / Amazfit",    how: "Google Fit",  color: "emerald" },
              { icon: "⌚", label: "Samsung Galaxy Watch", how: "Google Fit",  color: "emerald" },
              { icon: "🏃", label: "Garmin",               how: "Google Fit",  color: "emerald" },
              { icon: "🍎", label: "Apple Watch",          how: "Manual export", color: "yellow" },
            ].map((d) => (
              <div
                key={d.label}
                className={`flex items-center gap-1.5 px-3 py-1.5 rounded-full border ${
                  d.color === "emerald"
                    ? "bg-emerald-500/10 border-emerald-500/30 text-emerald-300"
                    : "bg-yellow-500/10 border-yellow-500/30 text-yellow-300"
                }`}
              >
                <span>{d.icon}</span>
                <span className="font-semibold">{d.label}</span>
                <span className="opacity-60">· {d.how}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Status banner */}
        {status === "loading" && (
          <div className="p-4 bg-blue-500/10 border border-blue-500/30 rounded-xl text-blue-400 text-center mb-6 animate-pulse">
            {message}
          </div>
        )}
        {status === "error" && (
          <div className="p-4 bg-red-500/10 border border-red-500/40 rounded-xl text-red-400 text-center mb-6">
            {message}
          </div>
        )}

        {/* Fetched data preview */}
        {status === "success" && fetched && (
          <div className="mb-8 p-6 bg-emerald-500/5 border border-emerald-500/30 rounded-2xl">
            <div className="flex items-center justify-between mb-4">
              <p className="text-emerald-400 font-bold">✓ {message}</p>
              <button
                onClick={handleUseFetchedData}
                className="bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-black py-2.5 px-6 rounded-xl text-sm transition-all"
              >
                Use This Data for Analysis →
              </button>
            </div>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
              {dataRows.map((r) => (
                <div key={r.label} className="p-3 bg-slate-800 rounded-xl">
                  <p className="text-slate-500 text-xs mb-1">{r.icon} {r.label}</p>
                  <p className="text-white font-bold text-sm">{r.value}</p>
                </div>
              ))}
            </div>
            {dataRows.length === 0 && (
              <p className="text-slate-400 text-sm">No health metrics found in the connected account for the past 7 days.</p>
            )}
          </div>
        )}

        {/* Source cards */}
        <div className="grid md:grid-cols-2 gap-5 mb-8">

          {/* Google Fit */}
          <SourceCard
            icon="🏃"
            name="Google Fit"
            description="Steps, weight, heart rate, sleep — via your Google account"
            badge="Free"
            onClick={connectGoogleFit}
          >
            <p className="text-slate-500 text-xs">
              Works with Android watches, Wear OS, Fitbit (if synced), and most fitness apps that export to Google Fit.
            </p>
          </SourceCard>

          {/* Fitbit */}
          <SourceCard
            icon="📱"
            name="Fitbit"
            description="Direct Fitbit API — steps, sleep stages, heart rate, weight"
            badge={FITBIT_CLIENT_ID ? "Free" : "Setup needed"}
            onClick={connectFitbit}
          >
            <p className="text-slate-500 text-xs">
              {FITBIT_CLIENT_ID
                ? "Connect your Fitbit account directly."
                : "Requires a free Fitbit developer app. See setup instructions below."}
            </p>
          </SourceCard>

          {/* Apple Health / Samsung / Garmin */}
          <SourceCard
            icon="🍎"
            name="Apple Watch / iPhone"
            description="Export from Apple Health app — takes ~2 minutes"
            badge="Manual export"
          >
            <ol className="text-slate-500 text-xs space-y-1 list-decimal list-inside mt-1">
              <li>Open the <span className="text-slate-300">Health app</span> on your iPhone</li>
              <li>Tap your profile picture → <span className="text-slate-300">Export All Health Data</span></li>
              <li>Share the ZIP → extract it → open <code className="text-emerald-400">export.xml</code></li>
              <li>Use a converter or paste key values into the manual import below</li>
            </ol>
          </SourceCard>
        </div>

        {/* Manual import */}
        <div className="border border-slate-700 rounded-2xl overflow-hidden mb-8">
          <button
            onClick={() => setShowManual((p) => !p)}
            className="w-full p-5 bg-slate-800/60 flex items-center justify-between hover:bg-slate-800 transition-all"
          >
            <div className="flex items-center gap-3">
              <span className="text-xl">📋</span>
              <div className="text-left">
                <p className="text-white font-bold">Manual Import</p>
                <p className="text-slate-400 text-xs">Paste exported JSON from any fitness app</p>
              </div>
            </div>
            <span className="text-slate-400 text-sm">{showManual ? "▲ Hide" : "▼ Show"}</span>
          </button>

          {showManual && (
            <div className="p-5 border-t border-slate-700 space-y-4">
              <div className="p-4 bg-slate-900 rounded-xl">
                <p className="text-slate-400 text-xs font-bold mb-2 uppercase tracking-widest">Expected JSON format</p>
                <pre className="text-emerald-400 text-xs leading-relaxed overflow-x-auto">{`{
  "steps": 8500,
  "weight_kg": 72.5,
  "height_m": 1.75,
  "heart_rate": 68,
  "sleep_hours": 7.2,
  "glucose": 95,
  "blood_pressure": 78
}`}</pre>
              </div>
              <textarea
                className="w-full bg-slate-900 border border-slate-700 rounded-xl p-4 text-white text-sm font-mono outline-none focus:border-emerald-500 transition-colors resize-none"
                rows={8}
                placeholder="Paste your exported JSON here..."
                value={manualText}
                onChange={(e) => setManualText(e.target.value)}
              />
              <button
                onClick={handleManualImport}
                disabled={!manualText.trim()}
                className="w-full bg-emerald-500 hover:bg-emerald-400 disabled:opacity-50 text-slate-950 font-bold py-3 rounded-xl transition-all"
              >
                Import & Preview Data
              </button>
            </div>
          )}
        </div>

        {/* Fitbit setup instructions */}
        {!FITBIT_CLIENT_ID && (
          <div className="p-5 bg-slate-800/40 border border-slate-700 rounded-2xl">
            <p className="text-white font-bold mb-2">Setting up Fitbit Integration</p>
            <ol className="text-slate-400 text-sm space-y-1.5 list-decimal list-inside">
              <li>Go to <a href="https://dev.fitbit.com/apps/new" target="_blank" rel="noopener noreferrer" className="text-emerald-400 underline">dev.fitbit.com/apps/new</a> and create a free app</li>
              <li>Set OAuth 2.0 Application Type to <strong className="text-white">Personal</strong></li>
              <li>Set Callback URL to <code className="text-emerald-400 bg-slate-900 px-1 rounded">{window.location.origin}/smartwatch</code></li>
              <li>Copy your Client ID and add it to <code className="text-emerald-400 bg-slate-900 px-1 rounded">FITBIT_CLIENT_ID</code> in <code className="text-emerald-400 bg-slate-900 px-1 rounded">Smartwatch.jsx</code></li>
            </ol>
          </div>
        )}

        {/* Privacy note */}
        <p className="text-center text-slate-600 text-xs mt-8">
          🔒 All device data is processed locally in your browser. Nothing is sent to our servers except the final health metrics you choose to analyse.
        </p>
      </div>
    </div>
  );
}
