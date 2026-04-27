import React, { useState } from "react";
import { Eye, EyeOff } from "lucide-react";
import { Button } from "@/components/ui/button";
import { UI_TEXT } from "@/constants/text";
import { STYLES } from "./LoginForm.styles";

export function LoginForm({ onCancel }) {
  const [showPassword, setShowPassword] = useState(false);
  const { login: loginText } = UI_TEXT.auth;

  return (
    <div className="flex flex-col mt-4">
      <div className="space-y-5">
        {/* Email Field */}
        <div className="flex flex-col gap-1.5">
          <label htmlFor="email" className={`${STYLES.label} self-start`}>
            {loginText.emailLabel}
          </label>
          <input
            id="email"
            type="email"
            placeholder={loginText.emailPlaceholder}
            className={`${STYLES.input} ${STYLES.emailExtra}`}
          />
        </div>

        {/* Password Field */}
        <div className="flex flex-col gap-1.5">
          <div className="flex items-center justify-between">
            <label htmlFor="password" className={STYLES.label}>
              {loginText.passwordLabel}
            </label>
          </div>
          <div className="relative">
            <input
              id="password"
              type={showPassword ? "text" : "password"}
              placeholder={loginText.passwordPlaceholder}
              className={`${STYLES.input} ${STYLES.passwordExtra}`}
            />
            <button
              type="button"
              onClick={() => setShowPassword(!showPassword)}
              className={STYLES.eyeBtn}
            >
              {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
            </button>
          </div>
        </div>

        <button type="button" className={STYLES.forgotBtn}>
          {loginText.forgotPassword}
        </button>

        {/* Action Buttons */}
        <div className="flex flex-col gap-3 pt-2">
          <Button className={`${STYLES.btnBase} text-base hover:opacity-90`}>
            {loginText.signInBtn}
          </Button>
          <Button
            variant="ghost"
            className={`${STYLES.btnBase} border border-border/50 bg-muted hover:bg-muted/80`}
            onClick={onCancel}
            type="button"
          >
            {loginText.cancelBtn}
          </Button>
        </div>
      </div>

      {/* Sign Up Section */}
      <div className="mt-6 pt-6 border-t border-border/60 text-center">
        <p className="text-base text-muted-foreground mb-4">
          {loginText.noAccount}
        </p>
        <Button
          variant="outline"
          className={`${STYLES.btnBase} border-input bg-background hover:bg-accent hover:text-accent-foreground`}
        >
          {loginText.signUpBtn}
        </Button>
      </div>
    </div>
  );
}
