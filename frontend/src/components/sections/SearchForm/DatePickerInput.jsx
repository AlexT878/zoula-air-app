import { Controller } from "react-hook-form";
import { Field, FieldLabel, FieldError } from "../../ui/field";
import { Input } from "../../ui/input";
import { Calendar } from "lucide-react";
import { styles } from "./SearchForm.styles";

export default function DatePickerInput({ control, label, placeholders }) {
  return (
    <Controller
      name="departureDate"
      control={control}
      render={({ field, fieldState }) => (
        <Field className="lg:col-span-2" data-invalid={fieldState.invalid}>
          <FieldLabel className={styles.label}>{label}</FieldLabel>
          <div className="flex">
            <Input
              {...field}
              id="departure"
              placeholder={placeholders.departure}
              className={styles.inputSplitLeft}
              startIcon={Calendar}
              aria-invalid={fieldState.invalid}
            />
            <Controller
              name="returnDate"
              control={control}
              render={({ field: returnField, fieldState: returnState }) => (
                <Input
                  {...returnField}
                  id="return"
                  placeholder={placeholders.return}
                  className={styles.inputSplitRight}
                  startIcon={Calendar}
                  aria-invalid={returnState.invalid}
                />
              )}
            />
          </div>
          {fieldState.invalid && <FieldError errors={[fieldState.error]} />}
        </Field>
      )}
    />
  );
}
