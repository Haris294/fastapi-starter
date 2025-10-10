import React, { useEffect, useMemo, useState } from "react";

const API_BASE = import.meta.env.VITE_API_BASE || "/api";

export default function App() {
  const [items, setItems] = useState([]);
  const [form, setForm] = useState({ name: "", description: "" });
  const [loading, setLoading] = useState(false);
  const [msg, setMsg] = useState("");

  const headers = useMemo(() => ({ "Content-Type": "application/json" }), []);

  const fetchItems = async () => {
    const r = await fetch(`${API_BASE}/v1/items?limit=100`);
    if (!r.ok) throw new Error(`GET items failed: ${r.status}`);
    setItems(await r.json());
  };

  useEffect(() => {
    fetchItems().catch((e) => setMsg(String(e)));
  }, []);

  const createItem = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMsg("");
    try {
      const r = await fetch(`${API_BASE}/v1/items`, {
        method: "POST",
        headers,
        body: JSON.stringify(form),
      });
      if (r.status === 429) {
        setMsg("Rate limited (429). Pause a sec and try again.");
      } else if (!r.ok) {
        setMsg(`Create failed: ${r.status}`);
      } else {
        setForm({ name: "", description: "" });
        await fetchItems();
      }
    } catch (err) {
      setMsg(String(err));
    } finally {
      setLoading(false);
    }
  };

  const remove = async (id) => {
    setLoading(true);
    setMsg("");
    try {
      const r = await fetch(`${API_BASE}/v1/items/${id}`, { method: "DELETE" });
      if (!r.ok && r.status !== 204) setMsg(`Delete failed: ${r.status}`);
      else await fetchItems();
    } catch (err) {
      setMsg(String(err));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card">
      <h2>Haris Items <code className="badge">FastAPI</code></h2>
      <p style={{marginTop: -8}}>
        API: <code>{API_BASE}</code>
      </p>

      <form onSubmit={createItem}>
        <input
          placeholder="Name"
          value={form.name}
          onChange={(e) => setForm((f) => ({ ...f, name: e.target.value }))}
          required
        />
        <input
          placeholder="Description"
          value={form.description}
          onChange={(e) => setForm((f) => ({ ...f, description: e.target.value }))}
        />
        <button disabled={loading} type="submit">Add</button>
      </form>

      {msg && <p style={{color:"#b00"}}>{msg}</p>}

      <ul style={{marginTop: 12}}>
        {items.map((it) => (
          <li key={it.id}>
            <div>
              <strong>{it.name}</strong>
              {it.description ? <> — <span>{it.description}</span></> : null}
            </div>
            <button onClick={() => remove(it.id)} disabled={loading}>✕</button>
          </li>
        ))}
        {!items.length && <li style={{opacity:.6}}>no items yet — add one ↑</li>}
      </ul>
    </div>
  );
}
