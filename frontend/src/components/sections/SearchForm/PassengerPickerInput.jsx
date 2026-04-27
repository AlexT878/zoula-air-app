import { useState } from "react";
import { Controller } from "react-hook-form";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import { Button } from "@/components/ui/button";
import { Field, FieldLabel, FieldError } from "../../ui/field";
import { UsersRound, Plus, Minus, Info } from "lucide-react";
import { styles } from "./SearchForm.styles";
import { cn } from "@/lib/utils";
import { useModal } from "@/context/ModalProvider";
import { CATEGORIES, MAX_PASSENGERS } from "@/constants/values";
import { UI_TEXT } from "@/constants/text";

export default function PassengerPicker({ control, label }) {
  const { terms: passengerTerms } = UI_TEXT.hero.inputs.passengers;
  const { modal } = UI_TEXT;
  const { alerts } = UI_TEXT;
  const [isPopoverOpen, setIsPopoverOpen] = useState(false);
  const { openModal } = useModal();
  const [counts, setCounts] = useState({
    adults: 1,
    youngAdults: 0,
    children: 0,
    infants: 0,
  });

  const totalPassengers = Object.values(counts).reduce(
    (sum, current) => sum + current,
    0,
  );

  const updateCount = (category, delta, onChange) => {
    const newCount = counts[category] + delta;

    // Conditions to gray out buttons
    if (delta > 0 && totalPassengers >= MAX_PASSENGERS) return;
    if (category === "adults" && newCount < 1) return;
    if (category !== "adults" && newCount < 0) return;

    if (category === "infants" && counts.infants === 0 && newCount === 1) {
      openModal(modal.infant.title, modal.infant.text);
      setIsPopoverOpen(false);
    }

    const newCounts = { ...counts, [category]: newCount };
    setCounts(newCounts);

    onChange(formatPassengerLabel(newCounts));
  };

  const formatPassengerLabel = (counts) => {
    const { adults, youngAdults, children, infants } = counts;
    const othersCount = youngAdults + children + infants;

    let labelText = `${adults} ${adults === 1 ? passengerTerms.adult_singular : passengerTerms.adult_plural}`;

    if (othersCount > 0) {
      labelText += `, ${othersCount} ${othersCount === 1 ? passengerTerms.other_singular : passengerTerms.other_plural}`;
    }

    return labelText;
  };

  return (
    <>
      <Controller
        name="passengers"
        control={control}
        render={({ field, fieldState }) => (
          <Field data-invalid={fieldState.invalid}>
            <FieldLabel className={styles.label}>{label}</FieldLabel>

            <Popover open={isPopoverOpen} onOpenChange={setIsPopoverOpen}>
              <PopoverTrigger asChild>
                <Button
                  variant="outline"
                  role="combobox"
                  className={cn(
                    styles.inputDefault,
                    "w-full justify-start px-3",
                    "font-normal text-sm text-foreground tracking-normal",
                    "hover:bg-white hover:text-foreground data-[state=open]:bg-white",
                    "focus-visible:ring-offset-0",
                    "data-[state=open]:border-gray-400/80 data-[state=open]:ring-0 data-[state=open]:z-10",
                  )}
                >
                  <UsersRound className="mr-2 h-4 w-4 shrink-0 opacity-50 text-muted-foreground" />
                  {field.value || "1 Adult"}
                </Button>
              </PopoverTrigger>

              <PopoverContent
                className="w-96 p-4"
                align="start"
                side="bottom"
                avoidCollisions={false}
              >
                <div className="space-y-4">
                  {CATEGORIES.map((cat) => (
                    <div
                      key={cat.id}
                      className="flex items-center justify-between"
                    >
                      <div>
                        <p className="text-sm font-bold leading-none">
                          {cat.label}
                        </p>
                        <p className="text-xs text-muted-foreground mt-1">
                          {cat.sub}
                        </p>
                      </div>

                      <div className="flex items-center gap-3">
                        <Button
                          type="button"
                          variant="outline"
                          size="icon"
                          className="h-8 w-8 rounded-full"
                          onClick={() =>
                            updateCount(cat.id, -1, field.onChange)
                          }
                          disabled={
                            (cat.id === "adults" && counts.adults <= 1) ||
                            (cat.id !== "adults" && counts[cat.id] <= 0)
                          }
                        >
                          <Minus className="h-3 w-3" />
                        </Button>

                        <span className="w-4 text-center font-medium">
                          {counts[cat.id]}
                        </span>

                        <Button
                          type="button"
                          variant="outline"
                          size="icon"
                          className="h-8 w-8 rounded-full"
                          onClick={() => updateCount(cat.id, 1, field.onChange)}
                          disabled={totalPassengers >= MAX_PASSENGERS}
                        >
                          <Plus className="h-3 w-3" />
                        </Button>
                      </div>
                    </div>
                  ))}
                </div>

                {totalPassengers >= MAX_PASSENGERS && (
                  <div className="mt-4 flex items-start gap-3 rounded-lg border border-red-200 bg-red-50 p-3 text-sm text-black">
                    <Info className="mt-0.5 h-5 w-5 shrink-0 text-red-600" />
                    <p className="leading-relaxed">
                      {alerts.maximum_passangers}
                    </p>
                  </div>
                )}
              </PopoverContent>
            </Popover>

            {fieldState.invalid && <FieldError errors={[fieldState.error]} />}
          </Field>
        )}
      />
    </>
  );
}
