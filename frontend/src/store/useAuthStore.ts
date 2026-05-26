import { create } from 'zustand';
import { persist } from 'zustand/middleware';

export interface Usuario {
  id: number;
  nombre: string;
  email: string;
  roles: string[];
  created_at: string;
}

interface AuthState {
  usuario: Usuario | null;
  isAuthenticated: boolean;
  setUsuario: (usuario: Usuario | null) => void;
  logout: () => void;
  hasRole: (role: string) => boolean;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      usuario: null,
      isAuthenticated: false,

      setUsuario: (usuario) => {
        set({
          usuario,
          isAuthenticated: usuario !== null,
        });
      },

      logout: () => {
        set({
          usuario: null,
          isAuthenticated: false,
        });
      },

      hasRole: (role: string) => {
        const state = get();
        return state.usuario?.roles.includes(role) ?? false;
      },
    }),
    {
      name: 'auth-storage',
    }
  )
);
