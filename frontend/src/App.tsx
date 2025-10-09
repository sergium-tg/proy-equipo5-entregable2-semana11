
import { Outlet, NavLink } from "react-router-dom";

export default function App(){
  return (
    <div className="min-h-screen text-coffee-900">
      <div className="mx-auto max-w-7xl p-4 md:p-8">
        <header className="glass p-4 md:p-6 flex items-center justify-between">
          <div className="font-semibold text-xl">Gestión de Mantenimiento</div>
          <nav className="flex gap-2">
            <NavLink to="/" className="btn btn-ghost">Dashboard</NavLink>
            <NavLink to="/clientes" className="btn btn-ghost">Clientes</NavLink>
            <NavLink to="/tecnicos" className="btn btn-ghost">Técnicos</NavLink>
            <NavLink to="/ordenes" className="btn btn-ghost">Órdenes</NavLink>
            <NavLink to="/mantenimientos" className="btn btn-ghost">Mantenimientos</NavLink>
            <NavLink to="/relaciones" className="btn btn-ghost">Mto–Técnicos</NavLink>
          </nav>
        </header>
        <main className="mt-6"><Outlet/></main>
      </div>
    </div>
  );
}
