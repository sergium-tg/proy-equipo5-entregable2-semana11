
import { useQuery } from "@tanstack/react-query";
import { OrdenesAPI } from "@/services/ordenes";
import { MantenimientosAPI } from "@/services/mantenimientos";

export default function Dashboard(){
  const ordenes = useQuery({ queryKey:["ordenes"], queryFn: ()=>OrdenesAPI.getAll().then(r=>r.data) });
  const mantenimientos = useQuery({ queryKey:["mantenimientos"], queryFn: ()=>MantenimientosAPI.getAll().then(r=>r.data) });
  return (
    <section className="grid md:grid-cols-3 gap-4">
      <div className="card"><h2 className="text-lg font-semibold">Órdenes</h2><p>{ordenes.data?.length ?? 0}</p></div>
      <div className="card"><h2 className="text-lg font-semibold">Mantenimientos</h2><p>{mantenimientos.data?.length ?? 0}</p></div>
      <div className="card"><h2 className="text-lg font-semibold">Estado</h2><p className="text-coffee-700">Todo listo ☕️</p></div>
    </section>
  );
}
