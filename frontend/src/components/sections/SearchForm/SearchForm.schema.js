import * as z from "zod";

export const searchFormSchema = z.object({
  departure: z
    .string()
    .min(1, "Enter a departure city.")
    .max(32, "Departure location must be at most 32 characters."),
  arrival: z
    .string()
    .min(1, "Enter an arrival city.")
    .max(32, "Arrival location must be at most 32 characters."),
  departureDate: z.string().min(1, "Select a date."),
  returnDate: z.string().min(1, ""),
  passengers: z.string().min(1, "Required."),
});
