import { UI_TEXT } from "@/constants/text";
import * as z from "zod";

const { alerts } = UI_TEXT;
export const searchFormSchema = z.object({
  departure: z
    .string()
    .min(1, alerts.no_departure_city)
    .max(32, alerts.max_departure_city),
  arrival: z
    .string()
    .min(1, alerts.no_arrival_city)
    .max(32, alerts.max_arrival_city),
  departureDate: z.string().min(1, alerts.no_date),
  returnDate: z.string().min(1, ""),
  passengers: z.string().min(1, alerts.no_passangers),
});
