import React, { useState } from "react";
import { Eye, EyeOff } from "lucide-react";
import { Button } from "@/components/ui/button";
import { UI_TEXT } from "@/constants/text";
import { STYLES } from "./LoginForm.styles";
import { Controller, useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { loginFormSchema } from "./LoginFormSchema";
import { Field, FieldError, FieldLabel } from "../ui/field";
import { Input } from "../ui/input";
import { loginUser } from "@/services/authService";

export function LoginForm({ onCancel }) {
  const [showPassword, setShowPassword] = useState(false);
  const { login: loginText } = UI_TEXT.auth;
  const form = useForm({
    resolver: zodResolver(loginFormSchema),
    mode: "onSubmit",
    defaultValues: {
      email: "",
      password: "",
    },
  });

  const handleLogin = async (data) => {
    console.log(data.email);

    try {
      const userData = loginUser(data.email, data.password);
      console.log(userData);
    } catch (error) {
      console.log(error.message);
    }
  };

  return (
    <form
      onSubmit={form.handleSubmit(handleLogin)}
      className="flex flex-col mt-4"
    >
      <div className="space-y-5">
        {/* Email Field */}
        <Controller
          name="email"
          control={form.control}
          render={({ field, fieldState }) => (
            <Field>
              <FieldLabel
                htmlFor="email"
                className={`${STYLES.label} self-start`}
              >
                {loginText.emailLabel}
              </FieldLabel>
              <Input
                {...field}
                aria-invalid={fieldState.invalid}
                id="email"
                placeholder="name@example.com"
                className={`${STYLES.input} ${STYLES.emailExtra}`}
              />
              {fieldState.invalid && <FieldError errors={[fieldState.error]} />}
            </Field>
          )}
        ></Controller>

        {/* Password Field */}
        <Controller
          name="password"
          control={form.control}
          render={({ field, fieldState }) => (
            <Field>
              <div className="flex items-center justify-between">
                <FieldLabel htmlFor="password" className={STYLES.label}>
                  {loginText.passwordLabel}
                </FieldLabel>
              </div>
              <div className="relative">
                <Input
                  {...field}
                  id="password"
                  type={showPassword ? "text" : "password"}
                  placeholder={loginText.passwordPlaceholder}
                  aria-invalid={fieldState.invalid}
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
              {fieldState.invalid && <FieldError errors={[fieldState.error]} />}
            </Field>
          )}
        />

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
          type="submit"
          className={`${STYLES.btnBase} border-input bg-background hover:bg-accent hover:text-accent-foreground`}
        >
          {loginText.signUpBtn}
        </Button>
      </div>
    </form>
  );
}
