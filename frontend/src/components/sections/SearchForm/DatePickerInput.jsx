import { Controller } from "react-hook-form";
import { Field, FieldLabel, FieldError } from "../../ui/field";
import { Input } from "../../ui/input";
import { Calendar } from "lucide-react";
import { styles } from "./SearchForm.styles";
import { cn } from "@/lib/utils";

export default function DatePickerInput({ control, label, placeholders }) {
  return (
    <Controller
      name="departureDate"
      control={control}
      render={({ field, fieldState }) => (
        <Controller
          name="returnDate"
          control={control}
          render={({ field: returnField, fieldState: returnState }) => {
            const hasError = fieldState.invalid || returnState.invalid;

            return (
              <Field className="lg:col-span-2" data-invalid={hasError}>
                <FieldLabel className={styles.label}>{label}</FieldLabel>

                <div
                  className={cn(
                    "flex -space-x-px rounded-md isolate transition-shadow duration-200",
                    hasError && "ring-2 ring-destructive/20 z-10",
                  )}
                >
                  <Input
                    {...field}
                    id="departure"
                    placeholder={placeholders.departure}
                    className={cn(
                      styles.inputSplitLeft,
                      hasError &&
                        "border-destructive z-10 focus-visible:ring-0 focus-visible:border-destructive",
                    )}
                    startIcon={Calendar}
                    aria-invalid={fieldState.invalid}
                  />
                  <Input
                    {...returnField}
                    id="return"
                    placeholder={placeholders.return}
                    className={cn(
                      styles.inputSplitRight,
                      hasError &&
                        "border-destructive z-10 focus-visible:ring-0 focus-visible:border-destructive",
                    )}
                    startIcon={Calendar}
                    aria-invalid={returnState.invalid}
                  />
                </div>

                {fieldState.invalid ? (
                  <FieldError errors={[fieldState.error]} />
                ) : returnState.invalid ? (
                  <FieldError errors={[returnState.error]} />
                ) : null}
              </Field>
            );
          }}
        />
      )}
    />
  );
}
