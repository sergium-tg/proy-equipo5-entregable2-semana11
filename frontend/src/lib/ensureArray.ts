// src/lib/ensureArray.ts
export function ensureArray<T = any>(x: any): T[] {
  // ya es array
  if (Array.isArray(x)) return x as T[];

  // estructuras comunes { items: [...] } o { results: [...] }
  if (x && Array.isArray(x.items)) return x.items as T[];
  if (x && Array.isArray(x.results)) return x.results as T[];

  // si llega un objeto tipo diccionario, conviértelo a array de valores
  if (x && typeof x === "object") return Object.values(x) as T[];

  // todo lo demás: evita romper la UI
  return [];
}
