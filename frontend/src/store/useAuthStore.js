import { create } from "zustand";

export const useAuthStore = create((set) => ({
  user: null,
  accessToken: null,
  isAuthenticated: false,
  isInitializing: true,

  setAuth: (user, token) =>
    set({
      user,
      accessToken: token,
      isAuthenticated: user !== null && user !== undefined ? true : false,
      isInitializing: false,
    }),

  finishInitialization: () => set({ isInitializing: false }),

  logout: () =>
    set({
      user: null,
      accessToken: null,
      isAuthenticated: false,
    }),
}));
