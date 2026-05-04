import { Routes, Route } from "react-router-dom";
import MainLayout from "./components/layout/MainLayout";
import Home from "./pages/Home";
import { ModalProvider } from "./context/ModalProvider";
import TestMe from "./pages/TestMe";

function App() {
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
