import { Controller } from "react-hook-form";
import { Field, FieldLabel, FieldError } from "../../ui/field";
import { Input } from "../../ui/input";
import { Search } from "lucide-react";
import { styles } from "./SearchForm.styles";

export default function LocationInput({
  name,
  control,
  label,
  placeholder,
  id,
}) {
  return (
    <Controller
      name={name}
      control={control}
      render={({ field, fieldState }) => (
        <Field data-invalid={fieldState.invalid}>
          <FieldLabel htmlFor={id} className={styles.label}>
            {label}
          </FieldLabel>
          <Input
            {...field}
            aria-invalid={fieldState.invalid}
            id={id}
            placeholder={placeholder}
            className={styles.inputDefault}
            startIcon={Search}
          />
          {fieldState.invalid && <FieldError errors={[fieldState.error]} />}
        </Field>
      )}
    />
  );
}
