import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { Tabs, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Button } from "@/components/ui/button";
import { UI_TEXT } from "@/constants/text";
import { FieldGroup } from "../../ui/field";
import { styles } from "./SearchForm.styles";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { searchFormSchema } from "./SearchForm.schema";
import LocationInput from "./LocationInput";
import PassengerPicker from "./PassengerPickerInput";
import DatePickerInput from "./DatePickerInput";

export default function SearchForm() {
  const form = useForm({
    resolver: zodResolver(searchFormSchema),
    mode: "onSubmit",
    defaultValues: {
      departure: "",
      arrival: "",
      departureDate: "",
      returnDate: "",
      passengers: "1 Adult",
    },
  });
  const { hero } = UI_TEXT;

  function onSubmit(data) {
    console.log("Form Data:", data);
  }

  return (
    <Card className={styles.card}>
      <CardHeader className={styles.header}>
        <Tabs defaultValue="round-trip" className="w-fit">
          <TabsList className={styles.tabList}>
            {hero.options.map((item) => (
              <TabsTrigger
                key={item.value}
                value={item.value}
                className={styles.tabTrigger}
              >
                {item.text}
              </TabsTrigger>
            ))}
          </TabsList>
        </Tabs>
      </CardHeader>

      <CardContent className={styles.content}>
        <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
          <FieldGroup className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-6 items-start mb-6">
            <LocationInput
              name="departure"
              control={form.control}
              id="from"
              label={hero.inputs.from.label}
              placeholder={hero.inputs.from.placeholder}
            />

            <LocationInput
              name="arrival"
              control={form.control}
              id="to"
              label={hero.inputs.to.label}
              placeholder={hero.inputs.to.placeholder}
            />

            <DatePickerInput
              control={form.control}
              label={hero.inputs.departure.label}
              placeholders={{
                departure: hero.inputs.departure.placeholder,
                return: hero.inputs.return.placeholder,
              }}
            />

            <PassengerPicker
              control={form.control}
              label={hero.inputs.passengers.label}
            />
          </FieldGroup>

          <div className="flex justify-center pt-2">
            <Button type="submit" className={styles.submitBtn}>
              {hero.inputs.submit}
            </Button>
          </div>
        </form>
      </CardContent>
    </Card>
  );
}
