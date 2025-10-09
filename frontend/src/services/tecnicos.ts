
import { api } from "@/lib/api";

export interface Tecnico {
  id_tecnico: number;
  nombre: string;
  apellido: string;
  telefono?: string;
  especialidad?: string;
}

export interface CrearTecnico {
  id_tecnico: number;
  nombre: string;
  apellido: string;
  telefono?: string;
  especialidad?: string;
}

export interface UpdateTecnico extends Partial<CrearTecnico> {}

export const TecnicosAPI = {
  create: (data: CrearTecnico) => api.post("/tecnicos", data),
  getAll: () => api.get<Tecnico[]>("/tecnicos/todos"),
  getById: (id: number) => api.get<Tecnico>(`/tecnicos/${id}`),
  update: (id: number, data: UpdateTecnico) => api.put(`/tecnicos/${id}`, data),
  delete: (id: number) => api.delete(`/tecnicos/${id}`),
  search: (params?: {
    q?: string;
    sort?: "nombre" | "apellido";
    order?: "asc" | "desc";
    offset?: number;
    limit?: number;
  }) => api.get<Tecnico[]>("/tecnicos", { params }),
};
