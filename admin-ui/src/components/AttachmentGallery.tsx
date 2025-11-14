import { buildDocumentUrl, isImage } from "../utils";

type Props = {
  documents: string[];
  apiBase: string;
};

export function AttachmentGallery({ documents, apiBase }: Props) {
  if (!documents.length) return null;

  return (
    <div className="doc-gallery">
      {documents.map((doc, idx) => {
        const url = buildDocumentUrl(doc, apiBase);
        const label = doc.split("/").pop() || `Attachment ${idx + 1}`;
        if (isImage(doc)) {
          return (
            <div className="doc-item" key={doc + idx}>
              <img src={url} loading="lazy" alt={label} />
              <div className="meta">
                <span>{label}</span>
                <a href={url} target="_blank" rel="noreferrer">
                  Open
                </a>
              </div>
            </div>
          );
        }

        return (
          <div className="doc-item" key={doc + idx}>
            <div className="meta">
              <span>{label}</span>
              <a href={url} target="_blank" rel="noreferrer">
                Download
              </a>
            </div>
          </div>
        );
      })}
    </div>
  );
}

