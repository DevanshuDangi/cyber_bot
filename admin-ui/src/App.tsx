import { useEffect, useMemo, useState } from "react";
import type { Complaint } from "./types";
import { parseDocuments } from "./utils";
import { Stats } from "./components/Stats";
import { AttachmentGallery } from "./components/AttachmentGallery";

const DEFAULT_API = import.meta.env.VITE_API_BASE || "http://localhost:8000";

export default function App() {
  const [apiBase, setApiBase] = useState<string>(DEFAULT_API);
  const [complaints, setComplaints] = useState<Complaint[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [expanded, setExpanded] = useState<Record<number, boolean>>({});

  useEffect(() => {
    refresh();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  async function refresh() {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`${apiBase.replace(/\/+$/, "")}/_demo/reports`);
      if (!res.ok) {
        throw new Error(`API returned ${res.status}`);
      }
      const data = (await res.json()) as Complaint[];
      setComplaints(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : String(err));
    } finally {
      setLoading(false);
    }
  }

  const stats = useMemo(() => {
    const total = complaints.length;
    const submitted = complaints.filter((c) => c.status === "submitted").length;
    const inProgress = complaints.filter((c) => c.status === "in_progress").length;
    const resolved = complaints.filter((c) => c.status === "resolved").length;
    return { total, submitted, inProgress, resolved };
  }, [complaints]);

  function toggleRow(id: number) {
    setExpanded((prev) => ({ ...prev, [id]: !prev[id] }));
  }

  return (
    <div className="layout">
      <header className="card">
        <h1>1930 Cybercrime Admin Console</h1>
        <p>Review complaints, evidence and status at a glance.</p>
        <div className="controls">
          <input
            value={apiBase}
            onChange={(e) => setApiBase(e.target.value)}
            placeholder="API base (e.g. http://localhost:8000)"
          />
          <button onClick={refresh} disabled={loading}>
            {loading ? "Loading..." : "Refresh"}
          </button>
        </div>
        {error && (
          <div style={{ marginTop: 12, color: "#b91c1c" }}>
            Failed to load complaints: {error}
          </div>
        )}
      </header>

      <Stats {...stats} />

      <section className="card">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Ref #</th>
              <th>Type</th>
              <th>Category</th>
              <th>Name</th>
              <th>Phone</th>
              <th>Status</th>
              <th>Created</th>
            </tr>
          </thead>
          <tbody>
            {complaints.map((complaint) => {
              const docs = parseDocuments(complaint.documents);
              return (
                <FragmentRow
                  key={complaint.id}
                  complaint={complaint}
                  docs={docs}
                  expanded={!!expanded[complaint.id]}
                  toggle={() => toggleRow(complaint.id)}
                  apiBase={apiBase}
                />
              );
            })}
          </tbody>
        </table>
        {!complaints.length && !loading && (
          <p style={{ textAlign: "center", marginTop: 24 }}>No complaints yet.</p>
        )}
      </section>
    </div>
  );
}

type RowProps = {
  complaint: Complaint;
  docs: string[];
  expanded: boolean;
  toggle: () => void;
  apiBase: string;
};

function statusBadge(status: string) {
  const map: Record<string, string> = {
    submitted: "submitted",
    in_progress: "in_progress",
    resolved: "resolved",
    draft: "draft"
  };
  const cls = map[status] || "draft";
  return <span className={`badge ${cls}`}>{status.toUpperCase()}</span>;
}

function FragmentRow({ complaint, docs, expanded, toggle, apiBase }: RowProps) {
  return (
    <>
      <tr className="accordion-row" onClick={toggle}>
        <td>{complaint.id}</td>
        <td>{complaint.reference_number ?? "-"}</td>
        <td>{complaint.complaint_type || "-"}</td>
        <td>{complaint.main_category || "-"}</td>
        <td>{complaint.name || "-"}</td>
        <td>{complaint.phone_number || "-"}</td>
        <td>{statusBadge(complaint.status)}</td>
        <td>{new Date(complaint.created_at).toLocaleString()}</td>
      </tr>
      {expanded && (
        <tr>
          <td colSpan={8}>
            <div className="details-panel">
              <div className="detail-grid">
                <span className="label">WhatsApp ID</span>
                <span>{complaint.user?.wa_id || "-"}</span>

                <span className="label">Email</span>
                <span>{complaint.email_id || "-"}</span>

                <span className="label">District</span>
                <span>{complaint.district || "-"}</span>

                <span className="label">Fraud Type</span>
                <span>{complaint.fraud_type || "-"}</span>

                <span className="label">Sub Type</span>
                <span>{complaint.sub_type || "-"}</span>

                <span className="label">Updated</span>
                <span>
                  {complaint.updated_at
                    ? new Date(complaint.updated_at).toLocaleString()
                    : "-"}
                </span>
              </div>

              {docs.length > 0 && (
                <>
                  <h4>Evidence</h4>
                  <AttachmentGallery documents={docs} apiBase={apiBase} />
                </>
              )}
            </div>
          </td>
        </tr>
      )}
    </>
  );
}

