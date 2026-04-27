import React, { createContext, useContext, useState, useEffect } from "react";
import { Baby, X } from "lucide-react";
import { UI_TEXT } from "@/constants/text";

const ModalContext = createContext();

// eslint-disable-next-line react-refresh/only-export-components
export const useModal = () => useContext(ModalContext);

export const ModalProvider = ({ children }) => {
  const { modal } = UI_TEXT;
  const [isOpen, setIsOpen] = useState(false);
  const [modalData, setModalData] = useState({ title: "", description: "" });

  const openModal = (title, description) => {
    setModalData({ title, description });
    setIsOpen(true);
  };

  const closeModal = () => setIsOpen(false);

  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = "hidden";
    } else {
      document.body.style.overflow = "unset";
    }
    return () => {
      document.body.style.overflow = "unset";
    };
  }, [isOpen]);

  return (
    <ModalContext.Provider value={{ openModal, closeModal }}>
      {children}

      {isOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
          <div className="absolute inset-0 bg-black/60" onClick={closeModal} />

          <div
            className="relative w-full max-w-sm bg-white rounded-xl shadow-xl p-6"
            role="dialog"
            aria-modal="true"
          >
            <button
              onClick={closeModal}
              className="absolute top-4 right-4 p-1.5 text-gray-400 hover:bg-gray-100 hover:text-gray-900 rounded-full transition-colors"
            >
              <X className="w-5 h-5" />
            </button>

            <div className="flex items-center gap-3 mb-4">
              <div className="flex items-center justify-center w-10 h-10 rounded-full bg-blue-50 text-blue-600 shrink-0">
                <Baby className="w-6 h-6" />
              </div>
              <h2 className="text-lg font-semibold text-gray-900">
                {modalData.title}
              </h2>
            </div>

            <p className="text-[15px] text-gray-600 leading-relaxed mb-6">
              {modalData.description}
            </p>

            <button
              onClick={closeModal}
              className="w-full py-2.5 bg-zinc-900 text-white font-medium rounded-lg hover:bg-zinc-800 transition-colors"
            >
              {modal.got_it}
            </button>
          </div>
        </div>
      )}
    </ModalContext.Provider>
  );
};
