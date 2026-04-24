import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { Tabs, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Button } from "@/components/ui/button";
import { UI_TEXT } from "@/constants/text";
import { Field, FieldGroup, FieldLabel } from "../ui/field";
import { Input } from "../ui/input";
import { Search, Calendar, UsersRound } from "lucide-react";
import { styles } from "./SearchForm.styles";

export default function SearchForm() {
  const { hero } = UI_TEXT;

  function handleSubmit(e) {
    e.preventDefault();
    console.log("Handle submit");
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
        <form onSubmit={handleSubmit} className="space-y-6">
          <FieldGroup className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-6 items-end">
            <Field>
              <FieldLabel htmlFor="from" className={styles.label}>
                {hero.inputs.from.label}
              </FieldLabel>
              <Input
                id="from"
                placeholder={hero.inputs.from.placeholder}
                className={styles.inputDefault}
                startIcon={Search}
              />
            </Field>

            <Field>
              <FieldLabel htmlFor="to" className={styles.label}>
                {hero.inputs.to.label}
              </FieldLabel>
              <Input
                id="to"
                placeholder={hero.inputs.to.placeholder}
                className={styles.inputDefault}
                startIcon={Search}
              />
            </Field>

            <Field className="lg:col-span-2">
              <FieldLabel className={styles.label}>
                {hero.inputs.departure.label}
              </FieldLabel>
              <div className="flex">
                <Input
                  id="departure"
                  placeholder={hero.inputs.departure.placeholder}
                  className={styles.inputSplitLeft}
                  startIcon={Calendar}
                />
                <Input
                  id="return"
                  placeholder={hero.inputs.return.placeholder}
                  className={styles.inputSplitRight}
                />
              </div>
            </Field>

            <Field>
              <FieldLabel htmlFor="passengers" className={styles.label}>
                {hero.inputs.passengers.label}
              </FieldLabel>
              <Input
                id="passengers"
                placeholder={hero.inputs.passengers.placeholder}
                className={styles.inputDefault}
                startIcon={UsersRound}
              />
            </Field>
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
