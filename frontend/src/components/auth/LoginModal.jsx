import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
} from "@/components/ui/dialog";
import { LoginForm } from "./LoginForm";
import { UI_TEXT } from "@/constants/text";

export function LoginModal({ isOpen, setIsOpen }) {
  const { header } = UI_TEXT;
  const { modal } = UI_TEXT;

  return (
    <Dialog open={isOpen} onOpenChange={setIsOpen}>
      <DialogContent className="sm:max-w-[480px] p-6 sm:p-8">
        <DialogHeader className="mb-2">
          <DialogTitle className="text-3xl font-bold tracking-tight text-center text-foreground">
            {header.signIn}
          </DialogTitle>
          <DialogDescription className="text-center text-base text-muted-foreground mt-1.5">
            {modal.signIn.subtitle}
          </DialogDescription>
        </DialogHeader>

        <LoginForm onCancel={() => setIsOpen(false)} />
      </DialogContent>
    </Dialog>
  );
}
