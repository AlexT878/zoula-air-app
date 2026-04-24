import { Controller } from "react-hook-form";
import { Field, FieldLabel, FieldError } from "../../ui/field";
import { Input } from "../../ui/input";
import { UsersRound } from "lucide-react";
import { styles } from "./SearchForm.styles";

export default function PassengerPicker({ control, label, placeholder }) {
  return (
    <Controller
      name="passengers"
      control={control}
      render={({ field, fieldState }) => (
        <Field data-invalid={fieldState.invalid}>
          <FieldLabel htmlFor="passengers" className={styles.label}>
            {label}
          </FieldLabel>
          <Input
            {...field}
            id="passengers"
            placeholder={placeholder}
            className={styles.inputDefault}
            startIcon={UsersRound}
            aria-invalid={fieldState.invalid}
          />
          {fieldState.invalid && <FieldError errors={[fieldState.error]} />}
        </Field>
      )}
    />
  );
}
