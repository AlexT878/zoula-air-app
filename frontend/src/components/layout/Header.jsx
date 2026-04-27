import { Link } from "react-router-dom";
import { Plane } from "lucide-react";
import { Button } from "@/components/ui/button";
import { UI_TEXT } from "@/constants/text";
import { LoginModal } from "../auth/LoginModal";
import { useState } from "react";

export default function Header() {
  const { header } = UI_TEXT;
  const [isLoginOpen, setIsLoginOpen] = useState(false);

  return (
    <header className="absolute top-0 left-0 right-0 z-50 px-12 pt-6 pb-48 bg-gradient-to-b from-primary/100 via-primary/60 to-transparent">
      <nav className="mx-auto flex items-center justify-between">
        <Link to="/" className="flex items-center gap-2">
          <Plane className="w-8 h-8 text-white" />
          <span className="text-white text-xl font-bold">{header.logo}</span>
        </Link>

        <ul className="hidden md:flex items-center gap-8 text-white font-medium text-base">
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

        <Button
          variant="ghost"
          className="cursor-pointer text-white hover:text-white/70 hover:bg-transparent transition-colors tracking-wide font-medium text-base p-0 h-auto"
          onClick={() => setIsLoginOpen(true)}
        >
          {header.signIn}
        </Button>
        <LoginModal isOpen={isLoginOpen} setIsOpen={setIsLoginOpen} />
      </nav>
    </header>
  );
}
