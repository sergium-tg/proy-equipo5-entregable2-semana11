import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { MtoTecsAPI } from "@/services/mtoTecs";
import { ensureArray } from "@/lib/ensureArray";

export default function MtoTecs() {
  const qc = useQueryClient();

  const list = useQuery({
    queryKey: ["mtoTecs"],
    queryFn: async () => {
      const res = await MtoTecsAPI.getAll();
      return ensureArray<any>(res.data);
    },
  });

  const [form, setForm] = useState({ numero_mto: 0, id_tecnico: 0, rol: "" });

  const create = useMutation({
    mutationFn: () => MtoTecsAPI.create(form),
    onSuccess: () => {
      setForm({ numero_mto: 0, id_tecnico: 0, rol: "" });
      qc.invalidateQueries({ queryKey: ["mtoTecs"] });
    },
  });

  const remove = useMutation({
    mutationFn: (pair: { numero_mto: number; id_tecnico: number }) =>
      MtoTecsAPI.delete(pair.numero_mto, pair.id_tecnico),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["mtoTecs"] }),
  });

  return (
    <section className="space-y-4">
      <div className="card">
        <h1 className="page">Relaciones Mantenimiento–Técnico</h1>
      </div>

      <div className="card grid md:grid-cols-4 gap-2">
        <input
          className="input"
          placeholder="Número Mto"
          value={form.numero_mto}
          onChange={(e) =>
            setForm({ ...form, numero_mto: Number(e.target.value) })
          }
        />
        <input
          className="input"
          placeholder="ID Técnico"
          value={form.id_tecnico}
          onChange={(e) =>
            setForm({ ...form, id_tecnico: Number(e.target.value) })
          }
        />
        <input
          className="input"
          placeholder="Rol"
          value={form.rol}
          onChange={(e) => setForm({ ...form, rol: e.target.value })}
        />
        <button
          className="btn btn-primary"
          onClick={() => create.mutate()}
          disabled={!form.numero_mto || !form.id_tecnico}
        >
          Crear
        </button>
      </div>

      <div className="card">
        {list.isLoading && <p>Cargando…</p>}
        {list.isError && (
          <p className="text-red-600">No se pudo cargar la lista.</p>
        )}
        {!list.isLoading && !list.isError && (
          <table className="w-full text-left">
            <thead>
              <tr>
                <th>Mto</th>
                <th>Técnico</th>
                <th>Rol</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {(list.data ?? []).map((r: any, idx: number) => {
                const numero =
                  r.numero_mto ?? r.numero_mantenimiento ?? r.numero;
                const tec = r.id_tecnico ?? r.tecnico_id ?? r.id;
                return (
                  <tr key={idx} className="border-t">
                    <td>{numero}</td>
                    <td>{tec}</td>
                    <td>{r.rol ?? "—"}</td>
                    <td className="text-right">
                      <button
                        className="btn btn-ghost"
                        onClick={() => remove.mutate({ numero_mto: numero, id_tecnico: tec })}
                      >
                        Eliminar
                      </button>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        )}
      </div>
    </section>
  );
}
