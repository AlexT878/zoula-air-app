import { Link } from "react-router-dom";
import { Plane, User } from "lucide-react";
import { UI_TEXT } from "@/constants/text";
import { LoginModal } from "../auth/LoginModal";
import { useState } from "react";
import { useAuthStore } from "@/store/useAuthStore";
import { Spinner } from "@/components/ui/spinner";
import { logoutUser } from "@/services/authService";

export default function Header() {
  const { header } = UI_TEXT;
  const [isLoginOpen, setIsLoginOpen] = useState(false);
  const { user, isAuthenticated, isInitializing } = useAuthStore();

  function handleLogin() {
    if (!isAuthenticated && !isInitializing) {
      setIsLoginOpen(true);
    } else if (!isInitializing) {
      logoutUser();
    }
  }

  return (
    <header className="absolute top-0 left-0 right-0 z-50 px-12 pt-6 pb-48 bg-gradient-to-b from-primary/100 via-primary/60 to-transparent">
      <nav className="mx-auto grid grid-cols-3 items-center">
        <div className="flex justify-start">
          <Link to="/" className="flex items-center gap-2">
            <Plane className="w-8 h-8 text-white" />
            <span className="text-white text-xl font-bold">{header.logo}</span>
          </Link>
        </div>

        <ul className="hidden md:flex items-center justify-center gap-8 text-white font-medium text-base">
          {header.nav.map((item) => (
            <li key={item.path}>
              <Link
                to={item.path}
                className="hover:text-white/70 transition-colors tracking-wide"
              >
                {item.name}
              </Link>
            </li>
          ))}
        </ul>

        <div className="flex justify-end">
          <button
            className="flex items-center justify-center min-w-[100px] max-w-[200px] rounded-md border border-white p-0.5 px-2 box-border cursor-pointer bg-transparent hover:border-white/70 transition-colors group"
            onClick={handleLogin}
          >
            {isInitializing ? (
              <Spinner className="size-6 text-white" />
            ) : isAuthenticated ? (
              <div className="flex items-center overflow-hidden">
                <User
                  seize={18}
                  className="text-white group-hover:text-white/70 transition-colors flex-shrink-0"
                />
                <span className="text-white group-hover:text-white/70 transition-colors tracking-wide font-medium text-base pl-2 truncate">
                  {user?.first_name}
                </span>
              </div>
            ) : (
              <span className="text-white group-hover:text-white/70 transition-colors tracking-wide font-medium text-base whitespace-nowrap">
                {header.signIn}
              </span>
            )}
          </button>
        </div>

        <LoginModal isOpen={isLoginOpen} setIsOpen={setIsLoginOpen} />
      </nav>
    </header>
  );
}
