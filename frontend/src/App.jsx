import { Routes, Route } from "react-router-dom";
import MainLayout from "./components/layout/MainLayout";
import Home from "./pages/Home";
import { ModalProvider } from "./context/ModalProvider";
import { useEffect } from "react";
import { useAuthStore } from "./store/useAuthStore";
import { refreshAccessToken } from "./services/apiClient";

function App() {
  useEffect(() => {
    const initAuth = async () => {
      const wasLoggedIn = localStorage.getItem("was_logged_in") === "true";
      if (wasLoggedIn) {
        await refreshAccessToken();
      }
      useAuthStore.getState().finishInitialization();
    };
    initAuth();
  }, []);

  return (
    <ModalProvider>
      <Routes>
        <Route path="/" element={<MainLayout />}>
          <Route index element={<Home />} />
        </Route>
      </Routes>
    </ModalProvider>
  );
}

export default App;
