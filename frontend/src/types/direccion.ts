export interface DireccionEntrega {
  id: number;
  usuario_id: number;
  alias: string;
  calle: string;
  ciudad: string;
  provincia: string;
  codigo_postal: string;
  es_principal: boolean;
  created_at: string;
  updated_at: string;
  deleted_at: string | null;
}
