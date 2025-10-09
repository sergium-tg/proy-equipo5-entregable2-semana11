import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { useState } from "react";
import { TecnicosAPI, Tecnico, CrearTecnico } from "@/services/tecnicos";
import { ensureArray } from "@/lib/ensureArray";

export default function Tecnicos() {
  const qc = useQueryClient();
  const [search, setSearch] = useState("");
  const [form, setForm] = useState<CrearTecnico>({
    id_tecnico: 0,
    nombre: "",
    apellido: "",
    telefono: "",
    especialidad: "",
  });

  const list = useQuery({
    queryKey: ["tecnicos", search],
    queryFn: async () => {
      const res = search
        ? await TecnicosAPI.search({
            q: search,
            sort: "apellido",
            order: "asc",
            offset: 0,
            limit: 50,
          })
        : await TecnicosAPI.getAll();
      return ensureArray<Tecnico>(res.data);
    },
  });

  const create = useMutation({
    mutationFn: (data: CrearTecnico) => TecnicosAPI.create(data),
    onSuccess: () => {
      setForm({
        id_tecnico: 0,
        nombre: "",
        apellido: "",
        telefono: "",
        especialidad: "",
      });
      qc.invalidateQueries({ queryKey: ["tecnicos"] });
    },
  });

  const remove = useMutation({
    mutationFn: (id: number) => TecnicosAPI.delete(id),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["tecnicos"] }),
  });

  return (
    <section className="space-y-4">
      <div className="card">
        <h1 className="page">Técnicos</h1>
        <p className="text-coffee-700">Directorio y especialidades</p>
      </div>

      <div className="card flex gap-2">
        <input
          className="input flex-1"
          placeholder="Buscar por nombre o apellido"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
        <button
          className="btn btn-ghost"
          onClick={() => qc.invalidateQueries({ queryKey: ["tecnicos", search] })}
        >
          Buscar
        </button>
      </div>

      <div className="card grid md:grid-cols-5 gap-2">
        <input
          className="input"
          placeholder="ID"
          value={form.id_tecnico}
          onChange={(e) =>
            setForm({ ...form, id_tecnico: Number(e.target.value) })
          }
        />
        <input
          className="input"
          placeholder="Nombre"
          value={form.nombre}
          onChange={(e) => setForm({ ...form, nombre: e.target.value })}
        />
        <input
          className="input"
          placeholder="Apellido"
          value={form.apellido}
          onChange={(e) => setForm({ ...form, apellido: e.target.value })}
        />
        <input
          className="input"
          placeholder="Teléfono"
          value={form.telefono ?? ""}
          onChange={(e) => setForm({ ...form, telefono: e.target.value })}
        />
        <button
          className="btn btn-primary"
          onClick={() => create.mutate(form)}
          disabled={!form.id_tecnico || !form.nombre || !form.apellido}
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
                <th>ID</th>
                <th>Nombre</th>
                <th>Teléfono</th>
                <th>Especialidad</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {(list.data ?? []).map((t: Tecnico) => (
                <tr key={t.id_tecnico} className="border-t">
                  <td>{t.id_tecnico}</td>
                  <td>
                    {t.nombre} {t.apellido}
                  </td>
                  <td>{t.telefono ?? "—"}</td>
                  <td>{t.especialidad ?? "—"}</td>
                  <td className="text-right">
                    <button
                      className="btn btn-ghost"
                      onClick={() => remove.mutate(t.id_tecnico)}
                    >
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
