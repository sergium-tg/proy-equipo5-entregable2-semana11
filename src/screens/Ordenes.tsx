import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { OrdenesAPI, CrearOrden, Orden } from "@/services/ordenes";

// Helper ultradefensivo (por si no tienes src/lib/ensureArray.ts)
function toArray<T = any>(x: any): T[] {
  try {
    if (Array.isArray(x)) return x as T[];
    if (x && Array.isArray(x.items)) return x.items as T[];
    if (x && Array.isArray(x.results)) return x.results as T[];
    if (x && typeof x === "object") return Object.values(x) as T[];
    return [];
  } catch {
    return [];
  }
}

export default function Ordenes() {
  const qc = useQueryClient();
  const [raw, setRaw] = useState<any>(null); // para ver qué llega

  const list = useQuery({
    queryKey: ["ordenes"],
    queryFn: async () => {
      const res = await OrdenesAPI.getAll();
      setRaw(res.data);
      return toArray<Orden>(res.data);  // <- NUNCA devuelve algo que no sea array
    },
    retry: 0,
  });

  const [form, setForm] = useState<CrearOrden>({
    id_cliente: 0,
    tipo: "Mantenimiento",
    descripcion: "",
    fecha: new Date().toISOString(),
  });

  const create = useMutation({
    mutationFn: (data: CrearOrden) => OrdenesAPI.create(data),
    onSuccess: () => {
      setForm({
        id_cliente: 0,
        tipo: "Mantenimiento",
        descripcion: "",
        fecha: new Date().toISOString(),
      });
      qc.invalidateQueries({ queryKey: ["ordenes"] });
    },
  });

  const remove = useMutation({
    mutationFn: (consecutivo: number) => OrdenesAPI.delete(consecutivo),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["ordenes"] }),
  });

  const rows = toArray<Orden>(list.data); // <- lo volvemos a asegurar aquí también

  return (
    <section className="space-y-4">
      <div className="card">
        <h1 className="page">Órdenes</h1>
        <p className="text-coffee-700">Listado y creación</p>
      </div>

      <div className="card grid md:grid-cols-4 gap-2">
        <input
          className="input"
          placeholder="ID Cliente"
          value={form.id_cliente}
          onChange={(e) => setForm({ ...form, id_cliente: Number(e.target.value) })}
        />
        <input
          className="input"
          placeholder="Tipo"
          value={form.tipo || ""}
          onChange={(e) => setForm({ ...form, tipo: e.target.value })}
        />
        <input
          className="input"
          placeholder="Descripción"
          value={form.descripcion || ""}
          onChange={(e) => setForm({ ...form, descripcion: e.target.value })}
        />
        <button
          className="btn btn-primary"
          onClick={() => create.mutate(form)}
          disabled={!form.id_cliente}
        >
          Crear
        </button>
      </div>

      <div className="card">
        {list.isLoading && <p>Cargando…</p>}

        {list.isError && (
          <div>
            <p className="text-red-600 mb-2">
              No se pudo cargar el listado de órdenes.
            </p>
            <details className="text-xs text-coffee-700">
              <summary>Ver respuesta cruda</summary>
              <pre className="mt-2 whitespace-pre-wrap break-all">
                {JSON.stringify(raw, null, 2)}
              </pre>
            </details>
          </div>
        )}

        {!list.isLoading && !list.isError && rows.length === 0 && (
          <div>
            <p className="text-coffee-700">No hay órdenes.</p>
            <details className="text-xs text-coffee-700">
              <summary>Ver respuesta cruda</summary>
              <pre className="mt-2 whitespace-pre-wrap break-all">
                {JSON.stringify(raw, null, 2)}
              </pre>
            </details>
          </div>
        )}

        {!list.isLoading && !list.isError && rows.length > 0 && (
          <table className="w-full text-left">
            <thead>
              <tr>
                <th>Consecutivo</th>
                <th>ID Cliente</th>
                <th>Tipo</th>
                <th>Descripción</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {rows.map((o) => (
                <tr key={o.consecutivo} className="border-t">
                  <td>{o.consecutivo}</td>
                  <td>{o.id_cliente}</td>
                  <td>{o.tipo ?? "—"}</td>
                  <td>{o.descripcion ?? "—"}</td>
                  <td className="text-right">
                    <button className="btn btn-ghost" onClick={() => remove.mutate(o.consecutivo)}>
                      Eliminar
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </section>
  );
}
