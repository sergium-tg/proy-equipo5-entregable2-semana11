
import { api } from "@/lib/api";

export interface Mantenimiento {
  numero: number;
  consecutivo_orden: number;
  tipo?: string;
  descripcion: string;
  apertura: string;
  precio?: number;
  cierre?: string;
}

export interface CrearMantenimiento {
  consecutivo_orden: number;
  tipo?: string;
  descripcion: string;
  apertura: string; // ISO
  precio?: number;
}

export interface UpdateMantenimiento extends Partial<CrearMantenimiento> { cierre?: string; }

export const MantenimientosAPI = {
  create: (data: CrearMantenimiento) => api.post("/mantenimientos", data),
  update: (num: number, data: UpdateMantenimiento) => api.put(`/mantenimientos/${num}`, data),
  getAll: () => api.get<Mantenimiento[]>("/mantenimientos/todos"),
  delete: (num: number) => api.delete(`/mantenimientos/${num}`),
  search: (params?: {
    q?: string;
    order?: "asc" | "desc";
    offset?: number;
    limit?: number;
  }) => api.get<Mantenimiento[]>("/mantenimientos", { params }),
};
