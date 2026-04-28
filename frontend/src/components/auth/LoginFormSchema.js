import { UI_TEXT } from "@/constants/text";
import * as z from "zod";

const { alerts } = UI_TEXT;

export const loginFormSchema = z.object({
  email: z.email(alerts.invalid_email).trim().toLowerCase(),

  password: z
    .string()
    .min(8, alerts.password_min_length)
    .max(64, alerts.password_max_length),
});
