const IMAGE_REGEX = /\.(png|jpe?g|gif|bmp|webp)$/i;

export function parseDocuments(input: string | string[] | null | undefined) {
  if (!input) return [];
  if (Array.isArray(input)) return input;
  try {
    return JSON.parse(input);
  } catch {
    return [];
  }
}

export function buildDocumentUrl(doc: string, apiBase: string) {
  if (!doc) return "";
  if (/^https?:\/\//i.test(doc)) return doc;
  let relative = doc.replace(/^file:\/\//, "");
  const mediaIndex = relative.indexOf("/media/");
  if (mediaIndex >= 0) {
    relative = relative.slice(mediaIndex + 1); // drop leading slash
  }
  relative = relative.replace(/^\/+/, "");
  if (!relative.startsWith("media/")) {
    relative = `media/${relative.replace(/^media\//, "")}`;
  }
  const base = apiBase.replace(/\/+$/, "");
  return `${base}/${relative}`;
}

export function isImage(doc: string) {
  const clean = doc.split("?")[0];
  return IMAGE_REGEX.test(clean);
}

